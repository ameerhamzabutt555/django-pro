from django.db import models
from django.utils import timezone

# Create your models here.


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StockItems(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_ok = models.BooleanField('Can be Sold', default=True)
    purchase_ok = models.BooleanField('Can be Purchased', default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StockInward(models.Model):
    id = models.AutoField(primary_key=True)
    stock_item_id = models.ForeignKey(
        StockItems,
        on_delete=models.CASCADE,
    )  # (Foreign Key to StockItems.id)
    store_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
    )  # (Foreign Key to Stores.id)
    quantity = models.IntegerField(null=True)
    vendor_id = models.ForeignKey(
        Vendor, on_delete=models.CASCADE
    )  # reign Key to Suppliers.id)
    invoice_number = models.CharField(max_length=100, null=True)
    purchase_order_number = models.CharField(max_length=100, null=True)
    received_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number if it's not set
            self.invoice_number = self.generate_invoice_number()

        if not self.pk:
            
            Expenses.objects.create(
                store=self.store_id,
                description=f"Stock Inward - {self.stock_item_id.name}",
                ref_id= self.invoice_number,
                amount=self.stock_item_id.unit_price * self.quantity,
                date=timezone.now().date(),
            )

        super().save(*args, **kwargs)

        #   # Calculate the expense amount
        # expense_amount = self.stock_item_id.unit_price * self.quantity
          
        # expense_description = f"Stock Inward - {self.stock_item_id.name}"
        # expense_date = timezone.now().date()
      

        # expense = Expenses.objects.create(
        #         store=self.store_id,
        #         description=expense_description,
        #         ref_id= self.invoice_number,
        #         amount=expense_amount,
        #         date=expense_date,
        #     )
        # super().save(*args, **kwargs)

    def generate_invoice_number(self):
        # Generate invoice number using a specific format
        last_invoice = StockInward.objects.order_by("-id").first()
        last_id = last_invoice.id if last_invoice else 0
        new_id = last_id + 1

        vendor_id = self.vendor_id.vendor_id
        store_id = self.store_id.store_id
        return f"INV-VN-{vendor_id}-ST-{store_id}-QT-{self.quantity}-{new_id:05d}"

    


class StockOutward(models.Model):
    id = models.AutoField(primary_key=True)
    stock_item_id = models.ForeignKey(
        StockItems,
        on_delete=models.CASCADE,
    )
    store_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(null=True)
    customer_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=100, null=True)
    reason = models.TextField(null=True)
    outward_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            stock_inward = StockInward.objects.filter(
                stock_item_id=self.stock_item_id, store_id=self.store_id
            ).first()
            if stock_inward:
                stock_inward.quantity -= self.quantity
                stock_inward.save()
            self.recipient = self.generate_recipient_number()
        super().save(*args, **kwargs)

    def generate_recipient_number(self):
        # Generate invoice number using a specific format
        recipient = StockOutward.objects.order_by("-id").first()
        last_id = recipient.id if recipient else 0
        new_id = last_id + 1

        stock_item_id = self.stock_item_id.id
        store_id = self.store_id.store_id
        return f"INV-SIT-{stock_item_id}-ST-{store_id}-QT-{self.quantity}-{new_id:05d}"


class StockAdjustment(models.Model):
    id = models.AutoField(primary_key=True)
    stock_item_id = models.ForeignKey(
        StockItems,
        on_delete=models.CASCADE,
    )
    store_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(null=True)
    reason = models.TextField(null=True)
    adjusted_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    ref_id = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
