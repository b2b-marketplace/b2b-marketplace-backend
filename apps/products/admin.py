from django.contrib import admin

from .models import Category, Image, Product


class ImageInLine(admin.TabularInline):
    model = Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")
    search_fields = ("product",)
    list_filter = ("product",)
    empty_value_display = "-empty-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-empty-"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = (
        "user",
        "category",
        "sku",
        "name",
        "brand",
        "price",
        "wholesale_quantity",
        "video",
        "quantity_in_stock",
        "description",
        "manufacturer_country",
        "is_deleted",
        "created_at",
        "updated_at",
    )
    search_fields = ("sku", "name", "user", "category")
    list_filter = ("sku", "name", "user", "category", "is_deleted")
    empty_value_display = "-empty-"
    inlines = (ImageInLine,)
