from django.db import models
from month.models import MonthField
from django.utils import timezone


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, default=None, blank=True)
    department = models.CharField(max_length=100, default=None, blank=True)
    address = models.CharField(max_length=255, default=None, blank=True)
    cnic_number = models.CharField(max_length=100, default=None, blank=True)
    mobile_number_1 = models.CharField(max_length=100, default=None, blank=True)
    mobile_number_2 = models.CharField(max_length=100, default=None, blank=True)
    hire_date = models.DateField()
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.FloatField(default=0)
    medical = models.FloatField(default=0)
    mobile_bils = models.FloatField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = MonthField(default=timezone.now)
    basic_salary = models.FloatField(default=0)
    leaves = models.FloatField(default=0)
    absent = models.FloatField(default=0)
    late = models.FloatField(default=0)
    advance = models.FloatField(default=0)
    net_payable = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.month}"
