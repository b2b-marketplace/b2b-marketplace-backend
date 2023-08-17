import factory

from apps.baskets.models import Basket, BasketProduct
from apps.products.factories import ProductFactory
from apps.users.factories import CustomUserFactory


class BasketFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания объектов корзины."""

    class Meta:
        model = Basket

    user = factory.SubFactory(CustomUserFactory)


class BasketProductFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания объектов товаров в корзине."""

    class Meta:
        model = BasketProduct

    basket = factory.SubFactory(BasketFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
