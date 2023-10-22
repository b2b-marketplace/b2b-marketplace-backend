import random

import factory
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.translation import gettext as _

from apps.baskets.factories import BasketFactory, BasketProductFactory
from apps.deliveries.factories import DeliveryFactory, DeliveryMethodFactory
from apps.orders.factories import OrderFactory, OrderProductFactory
from apps.orders.models import Order
from apps.products.factories import CategoryFactory, ProductFactory
from apps.products.models import Product
from apps.users.factories import (
    CompanyFactory,
    CustomUserFactory,
    PhysicalPersonFactory,
)
from apps.users.models import Address, CustomUser
from config.settings import LANGUAGE_CODE


class Command(BaseCommand):
    help = _("Creating test data.")

    def create_users(self, number_max):
        physical_persons = PhysicalPersonFactory.create_batch(number_max)
        companies = CompanyFactory.create_batch(number_max)

        CustomUserFactory.create_batch(number_max, personal=factory.Iterator(physical_persons))
        CustomUserFactory.create_batch(
            number_max, is_company=True, company=factory.Iterator(companies)
        )

    def create_products(self, number_max):
        categories = CategoryFactory.create_batch(number_max)
        users = CustomUser.objects.filter(is_company=True, company__role="supplier")
        for user in users:
            category = random.choice(categories)
            ProductFactory.create_batch(
                number_max, user=user, category=category, create_image=True, create_video=True
            )

    def create_baskets_and_orders(self, number_min):
        products = list(Product.objects.all())
        users = CustomUser.objects.filter(Q(is_company=False) | Q(company__role="customer"))
        for user in users:
            basket = BasketFactory(user=user)
            order = OrderFactory(user=user)
            user_products = random.sample(products, k=random.randint(number_min, len(products)))
            for product in user_products:
                BasketProductFactory(basket=basket, product=product)
                OrderProductFactory(order=order, product=product)

    def create_deliveries(self, number_max):
        orders = list(Order.objects.all())
        addresses = list(Address.objects.all())
        delivery_methods = DeliveryMethodFactory.create_batch(number_max)

        for order, address, delivery_method in zip(orders, addresses, delivery_methods):
            DeliveryFactory.create_batch(
                number_max, order=order, address=address, delivery_method=delivery_method
            )

    def handle(self, *args, **options):
        number_min = 1
        number_max = 5

        try:
            with factory.Faker.override_default_locale(LANGUAGE_CODE):
                self.create_users(number_max)
                self.create_products(number_max)
                self.create_baskets_and_orders(number_min)

            self.stdout.write(self.style.SUCCESS(_("Test data created successfully!")))
        except Exception as exp:
            self.stdout.write(self.style.ERROR(_("Error: %s" % exp)))
