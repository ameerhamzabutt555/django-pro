from django.contrib import admin
from employee_module.models import Employee, Salary


class SalaryInline(admin.TabularInline):
    model = Salary
    extra = 0


class EmployeeAdmin(admin.ModelAdmin):
    inlines = [SalaryInline]

    list_display = ["id", "user", "hire_date", "created_at", "updated_at"]
    list_filter = [field.name for field in Employee._meta.fields]
    search_fields = list_display
    list_per_page = 25


class SalaryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Salary._meta.get_fields()]
    list_filter = [field.name for field in Salary._meta.fields]
    search_fields = ['amount', 'employee__user__username','date']
    list_per_page = 25


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
