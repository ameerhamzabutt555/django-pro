from django.contrib import admin

# Register your models here.

from django.db.models import Sum

from django.contrib import admin
from balance_sheets.models import ClientTransaction, VendorTransaction
from myapp.models import Client, Vendor
from import_export.admin import ExportActionMixin


class ClientTransactionAdmin(ExportActionMixin, admin.ModelAdmin):
    # form = TransactionAdminForm
    list_display = (
        "client",
        "date",
        "amount",
        "transaction_type",
        "refrence_number",
        "description",
        "running_balance",
        "calculate_total_balance",
        "created_at",
        "updated_at",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is for edit mode
            return [
                "amount",
                "calculate_total_balance",
                "running_balance",
                "date",
                "created_at",
                "updated_at",
            ]
        return [
            "calculate_total_balance",
            "running_balance",
        ]

    def calculate_total_balance(self, obj):
        balance = obj.client.opening_balance

        transactions = ClientTransaction.objects.filter(client=obj.client)
        for transaction in transactions:
            if transaction.transaction_type == "debit":
                balance -= transaction.amount
            else:
                balance += transaction.amount
        return balance

    calculate_total_balance.short_description = "client total balance"

    def save_model(self, request, obj, form, change):
        if change:
            obj.running_balance = self.calculate_total_balance(obj)

        super().save_model(request, obj, form, change)

        obj.running_balance = self.calculate_total_balance(obj)

        super().save_model(request, obj, form, change)

        client = Client.objects.get(pk=obj.client.client_id)
        client.total_balance = self.calculate_total_balance(obj)
        client.save()

    search_fields = list_display

    list_per_page = 25
    readonly_fields = [
        "running_balance",
        "calculate_total_balance",
        "created_at",
        "updated_at",
    ]


class VendorTransactionAdmin(ExportActionMixin, admin.ModelAdmin):
    # form = TransactionAdminForm
    list_display = (
        "vendor",
        "date",
        "amount",
        "transaction_type",
        "refrence_number",
        "description",
        "running_balance",
        "calculate_total_balance",
        "created_at",
        "updated_at"
        # "total_balance",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is for edit mode
            return [
                "amount",
                "calculate_total_balance",
                "running_balance",
                "date",
                "created_at",
                "updated_at",
            ]
        return [
            "calculate_total_balance",
            "running_balance",
        ]

    def calculate_total_balance(self, obj):
        balance = obj.vendor.opening_balance

        transactions = VendorTransaction.objects.filter(vendor=obj.vendor)
        for transaction in transactions:
            if transaction.transaction_type == "debit":
                balance += transaction.amount
            else:
                balance -= transaction.amount
        return balance

    calculate_total_balance.short_description = "vendor total balance"

    def save_model(self, request, obj, form, change):
        if change:
            obj.running_balance = self.calculate_total_balance(obj)

        super().save_model(request, obj, form, change)

        obj.running_balance = self.calculate_total_balance(obj)

        super().save_model(request, obj, form, change)

        vendor = Vendor.objects.get(pk=obj.vendor.vendor_id)
        vendor.total_balance = self.calculate_total_balance(obj)
        vendor.save()

    search_fields = list_display

    list_per_page = 25
    readonly_fields = [
        "running_balance",
        "calculate_total_balance",
        "created_at",
        "updated_at",
    ]


admin.site.register(ClientTransaction, ClientTransactionAdmin)
admin.site.register(VendorTransaction, VendorTransactionAdmin)
