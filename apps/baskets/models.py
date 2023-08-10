from django.contrib.auth import get_user_model
from django.db import models


class Basket(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user", verbose_name="Пользователь"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.user}"


class BasketProduct(models.Model):
    basket = models.OneToOneField(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product", verbose_name="Товар")
    quantity = models.PositiveIntegerField(related_name="product quantity", verbose_name="Количество товара")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def __str__(self):
        return f"{self.quantity} x {self.product} in Basket for User: {self.basket.user}"
