import factory

from apps.deliveries.models import Delivery, DeliveryMethod
from apps.orders.factories import OrderFactory
from apps.users.factories import AddressFactory


class DeliveryMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeliveryMethod

    name = factory.Sequence(lambda n: f"delivery{n}")
    description = factory.Faker("paragraph")
    slug = factory.Sequence(lambda n: f"slug{n}")
    price = factory.Faker("pydecimal", min_value=0, left_digits=3, right_digits=1)


class DeliveryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Delivery

    order = factory.SubFactory(OrderFactory)
    address = factory.SubFactory(AddressFactory)
    delivery_method = factory.SubFactory(DeliveryMethodFactory)
    delivery_date = factory.Faker("date_time")
