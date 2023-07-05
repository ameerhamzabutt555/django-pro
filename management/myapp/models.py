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
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
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


class Salaries(models.Model):
    salary_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
