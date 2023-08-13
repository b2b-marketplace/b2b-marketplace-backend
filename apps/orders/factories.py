import factory
from orders.models import Order, OrderProduct


class OrderFactory(factory.Factory):
    class Meta:
        model = Order


class OrderProductFactory(factory.Factory):
    class Meta:
        model = OrderProduct
