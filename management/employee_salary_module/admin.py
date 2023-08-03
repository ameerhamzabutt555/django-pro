from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Attendance, Salary
from decimal import Decimal
from django.db.models import Q, Sum
from datetime import date, timedelta
import calendar


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
    list_display = (
        "employee",
        "date",
        "working_hours",
        "extra_hours",
        "leave_type",
    )
    list_filter = ("employee", "date")
    search_fields = ("employee__first_name", "employee__last_name")

    actions = ["calculate_and_save_salary"]


class SalaryAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "month",
        "leave_quota",
        "monthly_paid_leaves",
        "monthly_unpaid_leaves",
        "total_working_days",
        "monthly_working_days",
        "payable_days",
        "over_time",
        "basic_salary",
        "overtime_payable",
        "allowance",
        "gross_payable",
        "net_payable",
    ]

    def save_model(self, request, obj, form, change):
        # Calculate the fields before saving the Salary instance

        # Calculate Total
        obj.basic_salary = obj.employee.monthly_income
        obj.allowance = obj.employee.allowance
        obj.total_working_days = self.calculate_total_working_days(obj)
        (
            leave_quota,
            monthly_working_days,
            monthly_paid_leaves,
            monthly_unpaid_leaves,
        ) = self.calculate_leaves(obj)
        obj.leave_quota = leave_quota
        obj.monthly_paid_leaves = monthly_paid_leaves
        obj.monthly_unpaid_leaves = monthly_unpaid_leaves
        obj.monthly_working_days = monthly_working_days
        obj.payable_days = monthly_working_days + monthly_paid_leaves
        overtime_payable, over_time = self.calculate_overtime(obj)
        obj.overtime_payable, obj.over_time = overtime_payable, over_time

        obj.gross_payable = float(
            float(obj.payable_days)
            * (float(obj.basic_salary) / float(obj.total_working_days))
            + float(obj.allowance)
            + float(overtime_payable)
        )

        obj.net_payable = float(obj.gross_payable) - float(
            obj.monthly_unpaid_leaves
        ) * (float(obj.basic_salary) / float(obj.total_working_days))

        # obj.working_days = self.calculate_working_days(obj)
        # obj.leaves = self.calculate_leaves(obj)
        # obj.attandence = obj.working_days - obj.leaves
        # obj.earned_salary = float(obj.working_days * (obj.basic_salary / 30))

        # obj.total_amount = (
        #     float(obj.basic_salary) + float(obj.allowance) + float(obj.over_time)
        # )
        # obj.net_payable = (
        #     float(obj.earned_salary) + float(obj.allowance) + float(obj.over_time)
        # )

        super().save_model(request, obj, form, change)

    def calculate_overtime(self, obj):
        over_time = 0
        employee_monthly_attendance = Attendance.objects.filter(
            employee=obj.employee,
            date__month=obj.month.month,
            date__year=obj.month.year,
        )

        for attendance in employee_monthly_attendance:
            if attendance.leave_type == Attendance.NO_LEAVE:
                over_time += attendance.extra_hours

        overtime_payable = (
            float(over_time)
            * 1.5
            * float(obj.employee.monthly_income / obj.total_working_days / 8)
        )

        return float(overtime_payable), float(over_time)

    def calculate_leaves(self, obj):
        leave_quota = 15
        monthly_working_days = 0
        monthly_paid_leaves = 0
        monthly_unpaid_leaves = 0
        total_paid_leaves = total_unpaid_leaves = 0

        short_attendance = 0

        employee_monthly_attendance = Attendance.objects.filter(
            employee=obj.employee,
            date__month=obj.month.month,
            date__year=obj.month.year,
        )

        employee_yealy_attendance = Attendance.objects.filter(
            Q(employee=obj.employee),
            Q(date__year=obj.month.year),
        )

        for attendance in employee_yealy_attendance:
            if attendance.leave_type == Attendance.PAID_LEAVE:
                total_paid_leaves += 1
            if attendance.leave_type == Attendance.UNPAID_LEAVE:
                total_unpaid_leaves += 1

        for attendance in employee_monthly_attendance:
            if attendance.leave_type == Attendance.NO_LEAVE:
                monthly_working_days += 1
            if attendance.leave_type == Attendance.PAID_LEAVE:
                monthly_paid_leaves += 1
            if attendance.leave_type == Attendance.UNPAID_LEAVE:
                monthly_unpaid_leaves += 1

        if total_paid_leaves > leave_quota:
            unpaid_leaves = total_paid_leaves - leave_quota
            monthly_unpaid_leaves = monthly_unpaid_leaves + unpaid_leaves
            leave_quota = 0
        else:
            leave_quota = leave_quota - total_paid_leaves
            pass

        return (
            leave_quota,
            monthly_working_days,
            monthly_paid_leaves,
            monthly_unpaid_leaves,
        )

    def calculate_total_working_days(self, obj):
        # Calculate the first day of the month
        first_day = obj.month.replace(day=1)

        # Calculate the last day of the month
        first_day, last_day = calendar.monthrange(obj.month.year, obj.month.month)
        return last_day


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Salary, SalaryAdmin)
