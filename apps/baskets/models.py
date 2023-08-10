from django.contrib.auth import get_user_model
from django.db import models


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user", verbose_name="User")

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"

    def __str__(self):
        return f"{self.user}"


class BasketProduct(models.Model):
    basket = models.OneToOneField(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product", verbose_name="Product")
    quantity = models.PositiveIntegerField(related_name="product quantity", verbose_name="Product quantity")

    class Meta:
        verbose_name = "Product in the basket"
        verbose_name_plural = "Products in the basket"

    def __str__(self):
        return f"{self.quantity} x {self.product} in Basket for User: {self.basket.user}"
