from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    PAID_LEAVE = "Paid"
    UNPAID_LEAVE = "Unpaid"
    NO_LEAVE = "None"

    LEAVE_CHOICES = [
        (PAID_LEAVE, "Paid Leave"),
        (UNPAID_LEAVE, "Unpaid Leave"),
        (NO_LEAVE, "No Leave"),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    working_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    leave_type = models.CharField(
        max_length=10, choices=LEAVE_CHOICES, default=NO_LEAVE
    )
    advance = models.FloatField(default=0)
    # Add other fields as needed (e.g., leave, late arrival, early departure, etc.)

    def __str__(self):
        return f"{self.employee} - {self.date}"
    
    def save(self, *args, **kwargs):
        if self.leave_type in [self.PAID_LEAVE, self.UNPAID_LEAVE]:
            # If leave_type is Paid or Unpaid, set working_hours to zero
            self.working_hours = 0
            self.extra_hours = 0
            self.advance = 0

        super().save(*args, **kwargs)


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField(default=None)
    basic_salary = models.FloatField(default=0)
    allowance = models.FloatField(default=0)
    total_working_days = models.FloatField(default=0)
    leave_quota = models.FloatField(default=15)
    monthly_paid_leaves = models.FloatField(default=0)
    monthly_unpaid_leaves = models.FloatField(default=0)
    monthly_working_days = models.FloatField(default=0)
    payable_days = models.FloatField(default=0)
    gross_payable = models.FloatField(default=0)
    over_time = models.FloatField(default=0)
    overtime_payable = models.FloatField(default=0)
    total_salary = models.FloatField(default=0)
    net_payable = models.FloatField(default=0)
    total_advance = models.FloatField(default=0)

    def __str__(self):
        return f"{self.employee} - {self.month}"
