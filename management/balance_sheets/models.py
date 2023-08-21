from django.db import models
from django.utils import timezone
from myapp.models import Client, Vendor

# Create your models here.


class ClientTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("debit", "Debit"),
        ("credit", "Credit"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    refrence_number = models.CharField(max_length=255)
    description = models.CharField(max_length=200)
    running_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.name} - {self.date} ({self.transaction_type})"


class VendorTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("debit", "Debit"),
        ("credit", "Credit"),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    refrence_number = models.CharField(max_length=255)
    description = models.CharField(max_length=200)
    running_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.name} - {self.date} ({self.transaction_type})"
