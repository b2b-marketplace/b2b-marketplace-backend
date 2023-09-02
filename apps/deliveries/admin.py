from django.contrib import admin

from apps.deliveries.models import Delivery, DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-empty-"


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("order", "address", "delivery_method", "delivery_date", "price")
    search_fields = ("order", "address", "delivery_method", "delivery_date")
    list_filter = ("order", "address", "delivery_method", "delivery_date")
    empty_value_display = "-empty-"
