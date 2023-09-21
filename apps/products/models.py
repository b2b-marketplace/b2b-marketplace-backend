from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, SoftDeleteMixin
from apps.products.validators import validate_video
from apps.users.validators import validate_user_is_supplier


def get_product_directory_path(instance, filename):
    """Функция для генерации пути сохранения файлов товаров и изображений.

    Args:
        instance: Экземпляр модели (Image, Video или Product).
        filename (str): Имя файла.

    Returns:
        str: Путь для сохранения файла в зависимости от типа экземпляра.

    Пример использования:
        path = get_product_directory_path(image_instance, 'example.jpg')
    """
    if isinstance(instance, Image):
        return f"products/{instance.product.category.slug}/{instance.product.sku}/images/{filename}"
    if isinstance(instance, Video):
        return f"products/{instance.product.category.slug}/{instance.product.sku}/videos/{filename}"
    if isinstance(instance, Product):
        return f"products/{instance.category.slug}/{instance.sku}/{filename}"


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Category name"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
    """Модель изображения."""

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Product"),
    )
    image = models.ImageField(
        upload_to=get_product_directory_path,
        null=True,
        verbose_name=_("Product image"),
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f"{self.product}"


class Video(models.Model):
    """Модель видео."""

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name=_("Product"),
    )
    video = models.FileField(
        upload_to=get_product_directory_path,
        blank=True,
        null=True,
        verbose_name=_("Product video"),
        validators=[validate_video],
    )

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __str__(self):
        return f"{self.product}"


class ProductManager(models.Manager):
    """Менеджер для модели Product."""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("user", "category")
            .prefetch_related("images", "videos")
        )


class Product(SoftDeleteMixin, BaseModel):
    """Модель товара."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        validators=[validate_user_is_supplier],
        related_name="suppliers",
        verbose_name=_("Product supplier"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="categories",
        verbose_name=_("Product category"),
    )
    sku = models.CharField(max_length=255, verbose_name=_("Product sku"))
    name = models.CharField(max_length=255, verbose_name=_("Product name"))
    brand = models.CharField(max_length=255, verbose_name=_("Product brand"))
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name=_("Product price"),
        validators=[MinValueValidator(0.01)],
    )
    wholesale_quantity = models.PositiveIntegerField(verbose_name=_("Product wholesale quantity"))
    quantity_in_stock = models.PositiveIntegerField(verbose_name=_("Products quantity in stock"))
    description = models.TextField(verbose_name=_("Product description"))
    manufacturer_country = models.CharField(
        max_length=255, verbose_name=_("Product manufacturer country")
    )

    objects = ProductManager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [models.Index(fields=("category",))]

    def __str__(self):
        return f"{self.name}"
