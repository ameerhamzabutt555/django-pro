from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from import_export.admin import ExportActionMixin
from django import forms
from django.db.models import Sum
from django.http import HttpResponse
from myapp.models import (
    Client,
    Expenses,
    Vendor,
    StockItems,
    StockInward,
    StockOutward,
)
from django.urls import path, reverse
from django.core.exceptions import ValidationError
from .forms import StockOutwardForm


class ClientAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "total_balance",
        "opening_balance",
        "email",
        "phone",
        "city",
        "state",
        "created_at",
        "updated_at",
    )
    readonly_fields = ["created_at", "updated_at"]
    search_fields = list_display
    list_per_page = 25


class VendorAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "total_balance",
        "opening_balance",
        "email",
        "phone",
        "city",
        "state",
        "created_at",
        "updated_at",
    )
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    search_fields = list_display
    list_per_page = 25


class ExpensesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "description",
        "ref_id",
        "amount",
        "date",
        "created_at",
        "updated_at",
    )
    readonly_fields = [
        "ref_id",
        "amount",
        "date",
        "created_at",
        "updated_at",
    ]
    search_fields = list_display
    list_per_page = 25

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is for edit mode
            return [
                "ref_id",
                "amount",
                "date",
                "created_at",
                "updated_at",
            ]
        return []


class StockItemsAdmin(ExportActionMixin, admin.ModelAdmin):
    def get_stock_inward(self, obj):
        return obj.stockinward_set.all().count()

    get_stock_inward.short_description = "Stock Inward Count"

    list_display = (
        "name",
        "description",
        "unit_price",
        "get_stock_inward",
        "total_quantity",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "name",
        "description",
        "unit_price",
        "total_quantity",
    ]
    list_per_page = 25

    readonly_fields = ("total_quantity", "get_stock_inward", "created_at", "updated_at")


class StockInwardAdmin(ExportActionMixin, admin.ModelAdmin):
    def unit_price(self, obj):
        return format_html("<b>{}</b>", obj.stock_item_id.unit_price)

    unit_price.short_description = "unit_price"

    def save_model(self, request, obj, form, change):
        if change:
            expence = Expenses.objects.filter(ref_id=obj.invoice_number).get()
            expence.amount = obj.stock_item_id.unit_price * obj.quantity
            expence.save()

        super().save_model(request, obj, form, change)

        stock = StockItems.objects.get(pk=obj.stock_item_id.id)
        stock.total_quantity = self.calculate_total_quantity(obj)
        stock.save()

    def calculate_total_quantity(self, obj):
        total_quantity = 0
        stockesInwords = StockInward.objects.filter(stock_item_id=obj.stock_item_id)

        for stock in stockesInwords:
            total_quantity += stock.quantity

        print("total quantity", total_quantity)

        return total_quantity

    list_display = [
        "id",
        "stock_item_id",
        "quantity",
        "vendor_id",
        "invoice_number",
        "purchase_order_number",
        "received_date",
        "unit_price",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "id",
        "stock_item_id",
        "quantity",
        "vendor_id",
        "invoice_number",
        "purchase_order_number",
        "received_date",
        "created_at",
        "updated_at",
    ]
    # search_fields = list_display
    list_per_page = 25

    readonly_fields = ["invoice_number", "unit_price", "created_at", "updated_at"]
    search_fields = ["stock_item_id", "invoice_number"]


class StockOutwardAdmin(ExportActionMixin, admin.ModelAdmin):
    def stock_quantity(self, obj):
        stock_quantity = StockItems.objects.get(pk=obj.stock_item_id.id)
        return stock_quantity.total_quantity

    def unit_price(self, obj):
        return format_html("{}", obj.stock_item_id.unit_price)

    def total_price(self, obj):
        print("obj.quantity", obj.quantity)
        if obj.quantity:
            return format_html("{}", obj.stock_item_id.unit_price * obj.quantity)
        else:
            return format_html("{}", obj.stock_item_id.unit_price * 0)

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
            stock = StockItems.objects.get(pk=obj.stock_item_id.id)

            stock.total_quantity = self.stock_quantity(obj) - quantity_difference

            # if stock.total_quantity <= 0:
            #     raise ValidationError("No corresponding stock is empty")

            stock.save()

        super().save_model(request, obj, form, change)

    form = StockOutwardForm
    stock_quantity.short_description = "stock_quantity"
    unit_price.short_description = "unit_price"

    list_display = [
        "stock_item_id",
        "quantity",
        "customer_id",
        "recipient",
        "reason",
        "outward_date",
    ]
    list_display.insert(4, "unit_price")
    list_display.insert(5, "total_price")
    list_display.append("stock_quantity")
    search_fields = list_display
    list_per_page = 25
    list_filter = [field.name for field in StockOutward._meta.fields]
    readonly_fields = [
        "recipient",
        "unit_price",
        "total_price",
        "created_at",
        "updated_at",
    ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(StockItems, StockItemsAdmin)
admin.site.register(StockInward, StockInwardAdmin)
admin.site.register(StockOutward, StockOutwardAdmin)
