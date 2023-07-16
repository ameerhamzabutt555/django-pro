from django.contrib import admin
from employee_module.models import Employee, Salary
from django.utils import timezone
import csv
from django.http import HttpResponse


class SalaryInline(admin.TabularInline):
    model = Salary
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Check if editing an existing employee
            return ["created_at", "updated_at"]
        else:  # Creating a new employee
            return []  # Allow editing all fields


class EmployeeAdmin(admin.ModelAdmin):
    inlines = [SalaryInline]

    list_display = [
        "id",
        "user",
        "salary_amount",
        "hire_date",
        "created_at",
        "updated_at",
    ]
    list_filter = [field.name for field in Employee._meta.fields]
    search_fields = list_display
    list_per_page = 25
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'

        writer = csv.writer(response)
        headers = [
            "ID",
            "User",
            "Salary Amount",
            "Hire Date",
            "Created At",
            "Updated At",
        ]
        writer.writerow(headers)

        for employee in queryset:
            row = [
                employee.id,
                str(employee.user),
                employee.salary_amount,
                str(employee.hire_date),
                str(employee.created_at),
                str(employee.updated_at),
            ]
            writer.writerow(row)

        return response

    export_to_csv.short_description = "Export to CSV"

    actions = [export_to_csv]

class SalaryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Salary._meta.get_fields()]
    list_filter = [field.name for field in Salary._meta.fields]
    search_fields = ['amount_paid', 'employee__user__username','date']
    list_per_page = 25
    readonly_fields = ["amount_paid", "created_at", "updated_at"]

    def save_model(self, request, obj, form, change):
        # Assign the monthly salary amount to the salary record
        print("Printjfjdfdsjhj", obj.employee.salary_amount)
        obj.amount_paid = obj.employee.salary_amount

        super().save_model(request, obj, form, change)
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="salaries.csv"'

        writer = csv.writer(response)
        headers = [field.name for field in Salary._meta.get_fields()]
        writer.writerow(headers)

        for salary in queryset:
            row = [
                getattr(salary, field.name, "")
                for field in Salary._meta.get_fields()
            ]
            writer.writerow(row)

        return response

    export_to_csv.short_description = "Export to CSV"

    actions = [export_to_csv]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
