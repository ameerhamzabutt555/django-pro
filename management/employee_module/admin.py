# from django.contrib import admin
# from employee_module.models import Employee, Salary
# from import_export.admin import ExportActionMixin


# class SalaryInline(admin.TabularInline):
#     model = Salary
#     extra = 0

#     def get_readonly_fields(self, request, obj=None):
#         if obj:  # Check if editing an existing employee
#             return ["created_at", "updated_at"]
#         else:  # Creating a new employee
#             return []  # Allow editing all fields


# class EmployeeAdmin(ExportActionMixin,admin.ModelAdmin):
#     inlines = [SalaryInline]

#     list_display = [
#         "id",
#         "user",
#         "designation",
#         "hire_date",
#         "created_at",
#         "updated_at",
#     ]
#     list_filter = [field.name for field in Employee._meta.fields]
#     search_fields = list_display
#     list_per_page = 25
# export_formats = ('csv','xls','tsv','ods','yaml','xlsx', 'json','html')

# class SalaryAdmin(ExportActionMixin,admin.ModelAdmin):
#     list_display = [field.name for field in Salary._meta.get_fields()]
#     list_filter = [field.name for field in Salary._meta.fields]
#     search_fields = ['net_payable', 'employee__user__username','date']
#     list_per_page = 25
#     readonly_fields = ["net_payable", "created_at", "updated_at"]

#     def save_model(self, request, obj, form, change):
#         obj.net_payable = obj.employee.salary_amount

#         super().save_model(request, obj, form, change)
# export_formats = ('csv','xls','tsv','ods','yaml','xlsx', 'json','html')

# admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(Salary, SalaryAdmin)



from django.contrib import admin
from employee_module.models import Employee, Salary
from import_export.admin import ExportActionMixin


class SalaryInline(admin.TabularInline):
    model = Salary
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Check if editing an existing employee
            return ["created_at", "updated_at"]
        else:  # Creating a new employee
            return []  # Allow editing all fields


class EmployeeAdmin(ExportActionMixin, admin.ModelAdmin):
    inlines = [SalaryInline]

    list_display = [
        "id",
        "user",
        "designation",
        "hire_date",
        "created_at",
        "updated_at",
    ]
    list_filter = [field.name for field in Employee._meta.fields]
    search_fields = list_display
    list_per_page = 25
    readonly_fields = ["created_at", "updated_at"]


class SalaryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [field.name for field in Salary._meta.get_fields()]
    list_filter = [field.name for field in Salary._meta.fields]
    search_fields = ['net_payable', 'employee__user__username', 'date']
    list_per_page = 25
    readonly_fields = ["employee", "working_days", "leave_taken", "month", "year", "net_payable"]

    def save_model(self, request, obj, form, change):
        obj.net_payable = obj.basic_salary + obj.allowance - obj.deductions
        super().save_model(request, obj, form, change)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
