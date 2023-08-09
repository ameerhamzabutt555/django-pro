from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Salary
from decimal import Decimal
from django.db.models import F, Q, Sum
from datetime import date, timedelta
from django.db import models
import calendar
from import_export.admin import ExportActionMixin


class EmployeeAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "designation",
        "department",
        "hire_date",
        "monthly_income",
        "allowance",
        "medical",
        "mobile_bils",
    )
    list_filter = ("designation", "department", "hire_date")
    search_fields = ("first_name", "last_name")


class SalaryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        "employee",
        "month",
        "basic_salary",
        "leaves",
        "absent",
        "late",
        "advance",
        "net_payable",
    ]

    readonly_fields = [
        "basic_salary",
    ]

    def save_model(self, request, obj, form, change):
        # Calculate the fields before saving the Salary instance

        # Calculate Total
        obj.basic_salary = float(obj.employee.monthly_income)

        obj.allowance = float(obj.employee.allowance)
        obj.medical = float(obj.employee.medical)
        obj.mobile_bils = float(obj.employee.mobile_bils)

        leaves_deduct = obj.leaves * (float(obj.employee.monthly_income) / 30)
        absent_deduct = obj.absent * (float(obj.employee.monthly_income) / 30) * 1.5
        late_deduct = obj.late * (float(obj.employee.monthly_income) / 30) * 1.5
        advance_deduct = obj.advance

        obj.net_payable = (
            float(obj.employee.monthly_income)
            - leaves_deduct
            - absent_deduct
            - late_deduct
            - advance_deduct
        ) + (obj.allowance + obj.medical + obj.mobile_bils) * 1.0

        super().save_model(request, obj, form, change)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
