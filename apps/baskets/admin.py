from django.contrib import admin

from apps.baskets.models import Basket, BasketProduct


@admin.register(Basket)
class BasketProductInline(admin.TabularInline):
    model = BasketProduct


@admin.register(BasketProduct)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("user",)
    search_fields = ("user__username", "product__name")
    inlines = [
        BasketProductInline,
    ]
