from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Order, OrderProduct


class OrderProductFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        self.unique_seller()

        for form in self.forms:
            if form.cleaned_data:
                price = form.cleaned_data["product"].price
                form.cleaned_data["price"] = price
                if form.instance.price is None:
                    form.instance.price = price

    def unique_seller(self):
        seller = set()
        for form in self.forms:
            if form.cleaned_data:
                seller.add(form.cleaned_data["product"].user)
        if len(seller) > 1:
            raise ValidationError(_("The order is placed with products from one seller"))


class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    extra = 1
    formset = OrderProductFormSet
    readonly_fields = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "updated_at")
    search_fields = ("user",)
    list_filter = ("user", "status")
    empty_value_display = "-empty-"
    inlines = (OrderProductInLine,)
