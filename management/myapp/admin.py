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
    Store,
    StockItems,
    StockInward,
    StockOutward,
    StockAdjustment,
)
from django.urls import path, reverse


class ClientAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "state")
    search_fields = list_display
    list_per_page = 25
    
export_formats = ('csv','xls','tsv','ods','yaml','xlsx', 'json','html')


class VendorAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "state")
    search_fields = list_display
    list_per_page = 25
      
export_formats = ('csv','xls','tsv','ods','yaml','xlsx', 'json','html')
class StockInwardInline(admin.TabularInline):
    model = StockInward
    extra = 0


class StoreAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ("name", "description", "location", "city", "state")
    search_fields = list_display
    list_per_page = 25

      
export_formats = ('csv','xls','tsv','ods','yaml','xlsx', 'json','html')
class ExpensesAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ("store", "description","ref_id", "amount", "date")
    search_fields = list_display
    list_per_page = 25
       


export_formats = ('csv','xls','tsv','ods','yaml','xlsx', 'json','html')
class StockInwardInline(admin.TabularInline):
    model = StockInward
    extra = 0


class StoreInline(admin.TabularInline):
    model = Store
    extra = 0


class StockItemsAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "unit_price",
        "get_stock_inward",
    )
    search_fields = list_display
    list_per_page = 25

    def get_stock_inward(self, obj):
        return obj.stockinward_set.all().count()

    get_stock_inward.short_description = "Stock Inward Count"
    
export_formats = ('csv','xls','tsv','ods','yaml','xlsx', 'json','html')


class StockInwardAdmin(ExportActionMixin, admin.ModelAdmin):


    def unit_price(self, obj):
        return format_html("<b>{}</b>", obj.stock_item_id.unit_price)
    
    def save_model(self, request, obj, form, change):

        if change:
            expence = Expenses.objects.filter(ref_id=obj.invoice_number).get()
            expence.amount = obj.stock_item_id.unit_price * obj.quantity
            expence.save()

        super().save_model(request, obj, form, change)


    readonly_fields = ("unit_price",)

    unit_price.short_description = "unit_price"

    list_display = [field.name for field in StockInward._meta.get_fields()]
    list_display.append("unit_price")

    list_filter = [field.name for field in StockInward._meta.fields]
    search_fields = list_display
    list_per_page = 25

    readonly_fields = [
        "invoice_number",
    ]


class StockOutwardAdmin(ExportActionMixin, admin.ModelAdmin):
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
    unit_price.short_description = "unit_price"

    list_display = [
        "store_id",
        "stock_item_id",
        "quantity",
        "customer_id",
        "recipient",
        "reason",
        "outward_date",
    ]
    list_display.insert(4, "unit_price")
    list_display.insert(5, "total_price")
    list_display.append("stock_inward_quantityce")
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
