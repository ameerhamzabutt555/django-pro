from django.contrib import admin
from sales_expense_module.models import Expenses

# Register your models here.


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ("expence_number", "description", "amount", "date")
    search_fields = list_display
    list_per_page = 25

admin.site.register(Expenses, ExpensesAdmin)
