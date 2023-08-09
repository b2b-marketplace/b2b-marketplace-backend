from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, SoftDeleteMixin


def product_directory_path(instance, filename):
    if isinstance(instance, Image):
        return "products/product_{0}".format(instance.product.id)
    return "products/product_{0}".format(instance.id)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Category name"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("Category parent"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        verbose_name=_("Category slug"),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Product"),
    )
    image = models.ImageField(
        upload_to=product_directory_path,
        null=True,
        verbose_name=_("Product image"),
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f"{self.product}"


class ProductManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_deleted=False)
            .select_related("user", "category")
            .prefetch_related("images")
        )


class Product(SoftDeleteMixin, BaseModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="suppliers",
        verbose_name=_("Product supplier"),
    )
    category = models.OneToOneField(
        Category, on_delete=models.SET_NULL, null=True, related_name="categories", verbose_name=_("Product category")
    )
    sku = models.CharField(max_length=255, verbose_name=_("Product sku"))
    name = models.CharField(max_length=255, verbose_name=_("Product name"))
    brand = models.CharField(max_length=255, verbose_name=_("Product brand"))
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=_("Product price"))
    wholesale_quantity = models.PositiveIntegerField(
        verbose_name=_("Product wholesale quantity"),
    )
    video = models.FileField(upload_to=product_directory_path, null=True, verbose_name=_("Product video"))
    quantity_in_stock = models.PositiveIntegerField(
        verbose_name=_("Products quantity in stock"),
    )
    description = models.TextField(
        verbose_name=_("Product description"),
    )
    manufacturer_country = models.CharField(
        max_length=255,
        verbose_name=_("Product manufacturer country"),
    )

    objects = ProductManager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [models.Index(fields=("category",))]

    def __str__(self):
        return f"{self.name}"
