import types

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


def copy_func(f, name=None):
    fn = types.FunctionType(
        f.__code__, f.__globals__, name or f.__name__, f.__defaults__, f.__closure__
    )
    fn.__dict__.update(f.__dict__)
    return fn


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "updated_at")
    search_fields = ("user",)
    list_filter = ("user", "status")
    empty_value_display = "-empty-"
    inlines = (OrderProductInLine,)

    def delete_queryset(self, request, queryset):
        Status = Order.Status
        for obj in queryset:
            obj.status = Status.CANCELED
            obj.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        name = "delete_selected"
        function, name, _short_description = actions[name]
        my_custom_delete_selected = copy_func(function, name)
        short_description = "Отмена выбранных заказов"
        del actions[name]
        actions[name] = (my_custom_delete_selected, name, short_description)
        return actions
