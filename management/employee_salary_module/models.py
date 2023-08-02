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
    # Add other fields as needed (e.g., leave, late arrival, early departure, etc.)

    def __str__(self):
        return f"{self.employee} - {self.date}"


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    duration = models.DateField(default=None)
    working_days = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    earned_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    over_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    attandence = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leaves = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_payable = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee} - {self.duration}"
