import factory

from apps.orders.models import Order, OrderProduct
from apps.products.factories import ProductFactory
from apps.users.factories import CustomUserFactory


class OrderFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания объектов заказа."""

    class Meta:
        model = Order

    user = factory.SubFactory(CustomUserFactory)
    status = factory.Faker(
        "random_element", elements=[choice[0] for choice in Order.Status.choices]
    )


class OrderProductFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания объектов товаров в заказе."""

    class Meta:
        model = OrderProduct

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
    discount = factory.Faker("pydecimal", left_digits=2, right_digits=2)
