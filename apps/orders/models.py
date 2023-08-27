from _decimal import ROUND_HALF_UP, Decimal
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.products.models import Product


class OrderManager(models.Manager):
    def get_related_queryset(self, user):
        return (
            self.filter(user=user)
            .select_related("user__company", "user__personal")
            .prefetch_related("orders__product__user__company")
            .order_by("-created_at")
        )


def validate_user(value):
    """Валидация, является ли пользователь покупателем."""
    user = get_object_or_404(get_user_model(), pk=value)
    if not (user.personal or user.company.role == "customer"):
        raise ValidationError(_("Only buyers can create orders."))


class Order(BaseModel):
    """Модель заказа."""

    class Status(models.TextChoices):
        """Статусы заказа."""

        CREATED = "CR", _("Created")
        UPDATED = "UP", _("Updated")
        PAID = "PA", _("Paid")
        IN_TRANSIT = "TR", _("In_transit")
        COMPLETED = "CO", _("Completed")
        CANCELED = "CA", _("Canceled")
        RETURNED = "RE", _("Returned")

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        validators=[validate_user],
        related_name="customer",
        verbose_name=_("Order owner"),
    )
    order_products = models.ManyToManyField(
        Product,
        blank=False,
        through="OrderProduct",
        related_name="order_products",
        verbose_name=_("Products"),
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.CREATED, verbose_name=_("Order status")
    )

    objects = OrderManager()

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        indexes = [models.Index(fields=("user",))]

    def __str__(self):
        return f"{self.user}"

    def delete(self):
        """Предотвращает удаление модели.

        Вместо непосредственного удаления, помечает запись отмененной (status = canceled).
        """
        self.status = self.Status.CANCELED
        self.save()


class OrderProduct(models.Model):
    """Модель товара в заказе."""

    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        related_name="orders",
        verbose_name=_("Order"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name="orders",
        verbose_name=_("Product in order"),
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Product quantity in order"))
    discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        verbose_name=_("Product discount"),
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = _("OrderProduct")
        verbose_name_plural = _("OrderProducts")
        indexes = [models.Index(fields=("order",))]
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="%(app_label)s_%(class)s_order_product_uniq",
            )
        ]

    def __str__(self):
        return f"{self.order} - {self.product}"

    @property
    def cost(self):
        cost = self.product.price * self.quantity
        return cost.quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)

    @property
    def cost_with_discount(self):
        cost = self.cost - self.cost * (self.discount / 100)
        return cost.quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)
