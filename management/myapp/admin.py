from django.contrib import admin
from .models import Client, Expenses, Vendor, Store, Salaries
from django.contrib import admin



class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'state')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'state')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location', 'city', 'state')

class SalariesAdmin(admin.ModelAdmin):
    list_display = ('employee', 'amount', 'date_paid')

class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('store', 'description', 'amount', 'date')
    

admin.site.register(Client, ClientAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Salaries, SalariesAdmin)
admin.site.register(Expenses, ExpensesAdmin)
