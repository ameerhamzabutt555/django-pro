from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ClientTransaction
from myapp.models import Client

admin.site.register(ClientTransaction)
