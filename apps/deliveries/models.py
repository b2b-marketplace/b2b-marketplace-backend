from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Order
from apps.users.models import Address


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Delivery method name"))
    description = models.CharField(max_length=255, verbose_name=_("Delivery method description"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Delivery method slug"))
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name=_("Delivery price"),
        validators=[validators.MinValueValidator(0)],
    )

    class Meta:
        verbose_name = _("Delivery method")
        verbose_name_plural = _("Delivery methods")
        indexes = [models.Index(fields=("slug",))]

    def __str__(self):
        return self.name


class Delivery(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        related_name="delivery_order",
        verbose_name=_("Delivery order"),
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
        related_name="delivery_address",
        verbose_name=_("Delivery address"),
    )
    delivery_method = models.ForeignKey(
        DeliveryMethod,
        on_delete=models.DO_NOTHING,
        related_name="delivery_method",
        verbose_name=_("Delivery method"),
    )
    delivery_date = models.DateTimeField()

    class Meta:
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")
        indexes = [models.Index(fields=("order",))]

    def __str__(self):
        return f"Delivery {self.delivery_method} of the {self.order} to the {self.address}"
