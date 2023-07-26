from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=100,default='Unknown')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hire_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    working_days = models.PositiveIntegerField(default=0)
    leave_taken = models.PositiveIntegerField(default=0)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leave_absent_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField(default=1)
    net_payable = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calculate the total salary based on the provided data
        total_salary = self.basic_salary + self.allowance
        total_deductions = self.advance + self.leave_absent_deduction + self.other_deductions
        self.net_payable = total_salary - total_deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pay Slip {self.employee.user.username} - {self.month}-{self.year}"

