from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product


class Basket(models.Model):
    """ Модель корзины. """

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user", verbose_name=_("User")
    )
    basket_products = models.ManyToManyField(Product, through="BasketProduct")

    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    def __str__(self):
        return f"{self.user}"


class BasketProduct(models.Model):
    """ Модель товара в корзине. """

    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name="basket", verbose_name=_("Basket")
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product", verbose_name=_("Product")
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Product quantity"))

    class Meta:
        verbose_name = _("Product in the basket")
        verbose_name_plural = _("Products in the basket")

    def __str__(self):
        return f"{self.quantity} x {self.product} in Basket for User: {self.basket.user}"
