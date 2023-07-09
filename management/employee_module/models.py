from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    hire_date = models.DateField(default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Salary of {self.employee.user.username} - {self.amount}"
