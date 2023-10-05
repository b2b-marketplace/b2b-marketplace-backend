from _decimal import ROUND_HALF_UP, Decimal
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.products.models import Product
from apps.users.validators import validate_user_is_buyer


class OrderManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "user__company",
                "user__personal",
                "delivery_order",
                "delivery_order__address",
                "delivery_order__delivery_method",
            )
            .prefetch_related("orders__product__user__company", "orders__product__images")
            .order_by("-created_at")
        )

    def get_related_queryset(self, user):
        return self.filter(user=user)

    def get_supplier_orders(self, supplier):
        return self.filter(order_products__user=supplier).distinct()


class Order(BaseModel):
    """Модель заказа."""

    class Status(models.TextChoices):
        """Статусы заказа."""

        CREATED = "Created", _("Created")
        UPDATED = "Updated", _("Updated")
        PAID = "Paid", _("Paid")
        IN_TRANSIT = "Transit", _("In_transit")
        RECEIVED = "Received", _("Received")
        CANCELED = "Canceled", _("Canceled")
        RETURNED = "Returned", _("Returned")

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        validators=[validate_user_is_buyer],
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
        max_length=15,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name=_("Order status"),
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
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name=_("Product price"),
        validators=[validators.MinValueValidator(0)],
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
        cost = self.price * self.quantity
        return cost.quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)
