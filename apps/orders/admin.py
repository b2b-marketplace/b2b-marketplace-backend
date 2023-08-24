from django.contrib import admin

from apps.orders.models import Order, OrderProduct


class OrderProductInLine(admin.TabularInline):
    model = OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "updated_at")
    search_fields = ("user",)
    list_filter = (
        "user",
        "status",
    )
    empty_value_display = "-empty-"
    inlines = (OrderProductInLine,)
