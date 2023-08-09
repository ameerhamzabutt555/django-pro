from django import forms
from .models import StockInward, StockOutward, StockItems
from django.core.exceptions import ValidationError


# def validate_quantity(value):
#     if value > 10:
#         msg = "Price must be less than or equal to 1000"
#         raise ValidationError(msg)


class StockOutwardForm(forms.ModelForm):
    class Meta:
        model = StockOutward
        fields = "__all__"

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        stock_item_id = self.cleaned_data["stock_item_id"]
        stock = StockItems.objects.get(pk=stock_item_id.id)
        if quantity < 0:
            msg = "Quantity must be greater then zero"
            raise forms.ValidationError(msg)
        if stock.total_quantity <= 0:
            msg = "Sorry corresponding stock is empty"
            raise forms.ValidationError(msg)
        if quantity >= stock.total_quantity:
            msg = f"Quantity should be less than {stock.total_quantity}"
            raise forms.ValidationError(msg)
        return quantity
