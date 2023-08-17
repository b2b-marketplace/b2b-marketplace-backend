# from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.baskets.models import Basket, BasketProduct
from apps.users.models import CustomUser

from .basketproducts import BasketProductReadSerializer, BasketProductWriteSerializer

# User = get_user_model()


class BasketReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели Basket. Используется при чтении корзины.

    Для вычисления значения basket_products происходит обращение к данным
    промежуточной модели.

    """

    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    basket_products = BasketProductReadSerializer(read_only=True, many=True, source="basket")

    class Meta:
        model = Basket
        fields = ("id", "user", "basket_products")


class BasketCreateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Basket.

    Используется для создания корзины.
    """

    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Basket
        fields = "__all__"

    def create(self, user, instance=None):
        user = CustomUser.objects.get(id=1)
        if instance:
            return instance
        basket, _created = Basket.objects.get_or_create(user=user)
        return basket


class BasketWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Basket.

    Используется для добавления/обновления товаров в корзине.
    """

    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    basket_products = BasketProductWriteSerializer(many=True)

    class Meta:
        model = Basket
        fields = "__all__"

    def create_or_update_basket(self, user, instance=None):
        user = CustomUser.objects.get(id=1)
        if instance:
            return instance
        basket, _created = Basket.objects.get_or_create(user=user)
        return basket

    def create_products_quantity(self, basket_products, basket):
        products = set(basket.basket_products.values_list("id", flat=True))
        created_products = set()
        for product in basket_products:
            product_id = product["id"]
            if product_id in created_products or product_id in products:
                continue
            else:
                BasketProduct.objects.create(
                    basket=basket, product_id=product_id, quantity=product["quantity"]
                )
            created_products.add(product_id)

    def create(self, validated_data):
        basket_products = validated_data.pop("basket_products")
        basket = self.create_or_update_basket(validated_data)
        self.create_products_quantity(basket_products, basket)
        return basket

    def update(self, instance, validated_data):
        basket_products = validated_data.pop("basket_products")
        products = set(instance.basket_products.values_list("id", flat=True))

        # обновление существующих товаров или добавление новых товаров
        for product_data in basket_products:
            product_id = product_data["id"]
            quantity = product_data["quantity"]
            if product_id in products:
                # обновление количества товара
                BasketProduct.objects.filter(basket=instance, product_id=product_id).update(
                    quantity=quantity
                )
            else:
                # добавление нового товара
                self.create_products_quantity(basket_products, instance)

        # удаление товаров, которых больше нет в запросе
        products_to_remove = [
            product_id
            for product_id in products
            if product_id not in [product_data["id"] for product_data in basket_products]
        ]
        BasketProduct.objects.filter(basket=instance, product_id__in=products_to_remove).delete()
        return instance

    def to_representation(self, basket):
        representation = BasketReadSerializer(
            basket, context={"request": self.context.get("request")}
        )
        return representation.data
