from django.contrib import admin
from .models import Client, Expenses, Vendor, Store, Salaries

admin.site.register(Client)
admin.site.register(Expenses)
admin.site.register(Vendor)
admin.site.register(Store)
admin.site.register(Salaries)