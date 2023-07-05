from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from import_export.admin import ExportActionMixin
from .models import (
    Client,
    Expenses,
    Vendor,
    Store,
    Salaries,
    StockItems,
    StockInward,
    StockOutward,
    StockAdjustment,
)
from django.contrib import admin


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "state")


class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "state")


class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "location", "city", "state")


class SalariesAdmin(admin.ModelAdmin):
    list_display = ("employee", "amount", "date_paid")


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ("store", "description", "amount", "date")


class StockInwardInline(admin.TabularInline):
    model = StockInward
    extra = 0


class StockItemsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "unit_price",
        "get_stock_inward",
    )

    inlines = [StockInwardInline]

    def get_stock_inward(self, obj):
        return obj.stockinward_set.all().count()

    get_stock_inward.short_description = "Stock Inward Count"


class StockInwardAdmin(ExportActionMixin, admin.ModelAdmin):
    def unit_price(self, obj):
        return format_html("<b>{}</b>", obj.stock_item_id.unit_price)

    readonly_fields = ("unit_price",)

    unit_price.short_description = "unit_price"

    list_display = [field.name for field in StockInward._meta.get_fields()]
    list_display.append("unit_price")

    list_filter = [field.name for field in StockInward._meta.fields]


class StockOutwardAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StockOutward._meta.get_fields()]
    list_filter = [field.name for field in StockOutward._meta.fields]


class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StockAdjustment._meta.get_fields()]
    list_filter = [field.name for field in StockAdjustment._meta.fields]


admin.site.register(Client, ClientAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Salaries, SalariesAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(StockItems, StockItemsAdmin)
admin.site.register(StockInward, StockInwardAdmin)
admin.site.register(StockOutward, StockOutwardAdmin)
admin.site.register(StockAdjustment, StockAdjustmentAdmin)
