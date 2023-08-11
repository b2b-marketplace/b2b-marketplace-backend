from django.contrib import admin

from apps.baskets.models import Basket, BasketProduct


class BasketProductInline(admin.TabularInline):
    model = BasketProduct
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("basket", "product")
    list_filter = ("product",)
    search_fields = ("product",)
    inlines = [
        BasketProductInline,
    ]


admin.site.register(BasketProduct, BasketAdmin)
