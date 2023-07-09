from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from import_export.admin import ExportActionMixin
from django import forms
from django.db.models import Sum
from .models import (
    Client,
    Expenses,
    Vendor,
    Store,
    StockItems,
    StockInward,
    StockOutward,
    StockAdjustment,
)
from django.contrib import admin


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "state")
    search_fields = list_display
    list_per_page = 25


class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "state")
    search_fields = list_display
    list_per_page = 25


class StockInwardInline(admin.TabularInline):
    model = StockInward
    extra = 0


class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "location", "city", "state")
    search_fields = list_display
    list_per_page = 25

    inlines = [StockInwardInline]


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ("store", "description", "amount", "date")
    search_fields = list_display
    list_per_page = 25


class StockInwardInline(admin.TabularInline):
    model = StockInward
    extra = 0


class StoreInline(admin.TabularInline):
    model = Store
    extra = 0


class StockItemsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "unit_price",
        "get_stock_inward",
    )
    search_fields = list_display
    list_per_page = 25

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
    search_fields = list_display
    list_per_page = 25


class StockOutwardAdmin(ExportActionMixin, admin.ModelAdmin):
    print(StockOutward._meta.get_fields())
    print(StockInward._meta.get_fields())

    def stock_inward_quantityce(self, obj):
        stock_item_id = obj.stock_item_id
        store_id = obj.store_id
        stock_inward = StockInward.objects.get(
            stock_item_id=stock_item_id, store_id=store_id
        )
        return stock_inward.quantity

    def unit_price(self, obj):
        return format_html("{}", obj.stock_item_id.unit_price)

    def total_price(self, obj):
        return format_html("{}", obj.stock_item_id.unit_price * obj.quantity)

    readonly_fields = ("unit_price", "total_price")

    unit_price.short_description = "unit_price"

    def save_model(self, request, obj, form, change):
        # Check if the instance is being updated
        if change:
            original_outward = StockOutward.objects.get(pk=obj.pk)
            original_quantity = original_outward.quantity

            # Calculate the difference in quantity
            quantity_difference = obj.quantity - original_quantity

            print(
                "quantity_difference = obj.quantity - original_quantity",
                quantity_difference,
                obj.quantity,
                original_quantity,
            )
            # Get the corresponding StockInward instance
            stock_inward = StockInward.objects.get(
                stock_item_id=obj.stock_item_id, store_id=obj.store_id
            )

            stock_inward.quantity = stock_inward.quantity - quantity_difference
            stock_inward.save()

        super().save_model(request, obj, form, change)

    stock_inward_quantityce.short_description = "stock_inward_quantityce"

    list_display = [field.name for field in StockOutward._meta.get_fields()]
    list_display.insert(4, "unit_price")
    list_display.insert(5, "total_price")
    list_display.append("stock_inward_quantityce")
    search_fields = list_display
    list_per_page = 25
    list_filter = [field.name for field in StockOutward._meta.fields]


class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StockAdjustment._meta.get_fields()]
    list_filter = [field.name for field in StockAdjustment._meta.fields]
    search_fields = list_display
    list_per_page = 25


admin.site.register(Client, ClientAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(StockItems, StockItemsAdmin)
admin.site.register(StockInward, StockInwardAdmin)
admin.site.register(StockOutward, StockOutwardAdmin)
admin.site.register(StockAdjustment, StockAdjustmentAdmin)
