from django.contrib import admin
from .models import Employee, Attendance

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'designation', 'department', 'hire_date', 'monthly_income')
    list_filter = ('designation', 'department', 'hire_date')
    search_fields = ('first_name', 'last_name')

admin.site.register(Employee, EmployeeAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'working_hours', 'extra_hours','leave_type')
    list_filter = ('employee', 'date')
    search_fields = ('employee__first_name', 'employee__last_name')

admin.site.register(Attendance, AttendanceAdmin)
