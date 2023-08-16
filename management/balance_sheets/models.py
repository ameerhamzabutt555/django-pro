from django.db import models

from myapp.models import Client

# Create your models here.


class ClientTransaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.month} - {self.client.name}"
