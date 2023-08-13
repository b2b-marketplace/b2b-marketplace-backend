from django.contrib import admin

from apps.baskets.models import Basket, BasketProduct


class BasketProductInline(admin.TabularInline):
    model = BasketProduct
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("user",)
    search_fields = ("user",)
    empty_value_display = "-empty-"
    inlines = (BasketProductInline,)
