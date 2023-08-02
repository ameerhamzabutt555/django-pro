from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Attendance, Salary


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "designation",
        "department",
        "hire_date",
        "monthly_income",
        "allowance",
    )
    list_filter = ("designation", "department", "hire_date")
    search_fields = ("first_name", "last_name")


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "working_hours", "extra_hours", "leave_type")
    list_filter = ("employee", "date")
    search_fields = ("employee__first_name", "employee__last_name")


class SalaryAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "duration",
        "working_days",
        "basic_salary",
        "earned_salary",
        "over_time",
        "attandence",
        "leaves",
        "total_amount",
        "net_payable",
    )
    list_filter = ("employee",)
    search_fields = ("employee__first_name", "employee__last_name")

    readonly_fields = [
        "working_days",
        "basic_salary",
        "earned_salary",
        "over_time",
        "attandence",
        "leaves",
        "allowance",
        "total_amount",
        "net_payable",
    ]

    def save_model(self, request, obj, form, change):
        # Calculate the fields before saving the Salary instance

        # Calculate Total
        obj.basic_salary = obj.employee.monthly_income
        obj.allowance = obj.employee.allowance
        obj.over_time = self.calculate_overtime(obj)

        obj.working_days = self.calculate_working_days(obj)
        obj.leaves = self.calculate_leaves(obj)
        obj.attandence = obj.working_days - obj.leaves
        obj.earned_salary = float(obj.working_days * (obj.basic_salary / 30))

        obj.total_amount = (
            float(obj.basic_salary) + float(obj.allowance) + float(obj.over_time)
        )
        obj.net_payable = (
            float(obj.earned_salary) + float(obj.allowance) + float(obj.over_time)
        )

        super().save_model(request, obj, form, change)

    def calculate_working_days(self, obj):
        # Calculate working days based on the attendance records for the employee and duration
        # You'll need to implement this logic based on your requirements
        # Here's a sample implementation for the sake of demonstration
        total_working_days = 0
        attendances = Attendance.objects.filter(
            employee=obj.employee,
            date__month=obj.duration.month,
            date__year=obj.duration.year,
        )
        for attendance in attendances:
            if attendance.leave_type != Attendance.UNPAID_LEAVE:
                total_working_days += 1
        return total_working_days

    def calculate_overtime(self, obj):
        # Calculate overtime based on extra_hours in Attendance
        # You'll need to implement this logic based on your requirements
        # Here's a sample implementation for the sake of demonstration
        total_overtime_hours = 0
        attendances = Attendance.objects.filter(
            employee=obj.employee,
            date__month=obj.duration.month,
            date__year=obj.duration.year,
        )
        for attendance in attendances:
            total_overtime_hours += attendance.extra_hours
        print("total_overtime_hours", total_overtime_hours)
        return (float(total_overtime_hours) * float(1.5)) * float(
            obj.employee.monthly_income / 30 / 8
        )

    def calculate_leaves(self, obj):
        total_leaves = 0
        attendances = Attendance.objects.filter(
            employee=obj.employee,
            date__month=obj.duration.month,
            date__year=obj.duration.year,
        )

        for attendance in attendances:
            if attendance.leave_type == Attendance.UNPAID_LEAVE:
                total_leaves += 1

        return total_leaves


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Salary, SalaryAdmin)
