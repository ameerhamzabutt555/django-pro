from django.db import models
from django.utils import timezone

# Create your models here.


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    expence_number = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.expence_number:
            # Generate invoice number if it's not set
            self.expence_number = self.expence_number()

        super().save(*args, **kwargs)
    
    def expence_number(self):
        return f"EXP-{str(self.id).zfill(5)}"



class Sales(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
