from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from employee_salary_module.models import Employee, Salary
from decimal import Decimal
from django.db.models import F, Q, Sum
from datetime import date, timedelta
from django.db import models
import calendar
from import_export.admin import ExportActionMixin
from django.urls import reverse

import csv
from django.http import HttpResponse


class EmployeeAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "designation",
        "department",
        "hire_date",
        "monthly_income",
        "net_advance",
        "allowance",
        "medical",
        "mobile_bils",
    )
    list_filter = ("designation", "department", "hire_date")
    search_fields = ("first_name", "last_name")


class SalaryAdmin(ExportActionMixin, admin.ModelAdmin):
    def generate_pdf_link(self, obj):
        # Generate the URL for the PDF view
        pdf_url = reverse("render_pdf_view", args=[obj.id])
        return format_html('<a href="{}" target="_blank">&#x2193 PDF</a>', pdf_url)

    generate_pdf_link.short_description = "Download PDF"

    @admin.action(description="Generate CSV")
    def generateCSV(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        print("fealdis________________", field_names, queryset)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment;   filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
            print("ROW________________", row, queryset)

        # return response

    list_display = [
        "employee",
        "month",
        "basic_salary",
        "over_time",
        "over_time_payable",
        "leaves",
        "absent",
        "late",
        "advance",
        "advance_deduction",
        "net_payable",
        "generate_pdf_link",
    ]

    readonly_fields = [
        "basic_salary",
        "over_time_payable",
        "net_payable",
    ]
    actions = [generateCSV]

    def save_model(self, request, obj, form, change):
        # Calculate the fields before saving the Salary instance

        # Calculate Total
        obj.basic_salary = float(obj.employee.monthly_income)

        obj.allowance = float(obj.employee.allowance)
        obj.medical = float(obj.employee.medical)
        obj.mobile_bils = float(obj.employee.mobile_bils)

        obj.over_time_payable = (obj.over_time * float(obj.employee.overtime_rate)) * (
            float(obj.employee.monthly_income) / 30 / 8
        )

        if obj.is_late_deductable:
            late_deduct = obj.late * (float(obj.employee.monthly_income) / 30 / 8) * 1.5
        else:
            late_deduct = 0

        if obj.is_leaves_deductable:
            if obj.leaves > 0:
                obj.leaves = obj.leaves - 1
            leaves_deduct = obj.leaves * (float(obj.employee.monthly_income) / 30)
        else:
            leaves_deduct = 0
        if obj.is_absent_deductable:
            absent_deduct = obj.absent * (float(obj.employee.monthly_income) / 30) * 1.5
        else:
            absent_deduct = 0

        advance_deduct = (
            obj.employee.net_advance + obj.advance
        ) - obj.advance_deduction

        if not change:
            self.employee_obj = obj.employee
            self.employee_obj.net_advance = advance_deduct
            self.employee_obj.save()

        obj.net_payable = (
            float(obj.employee.monthly_income)
            - leaves_deduct
            - absent_deduct
            - late_deduct
            - obj.advance_deduction
        ) + (
            obj.allowance + obj.medical + obj.mobile_bils + obj.over_time_payable
        ) * 1.0

        super().save_model(request, obj, form, change)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
