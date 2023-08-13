import factory
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from apps.products.factories import CategoryFactory, ImageFactory, ProductFactory

# from orders.factories import OrderFactory, OrderProductFactory
from apps.users.factories import (
    AddressFactory,
    CompanyFactory,
    CustomUserFactory,
    PhoneNumberFactory,
    PhysicalPersonFactory,
)


class Command(BaseCommand):
    help = _("Creating test data.")

    def handle(self, *args, **options):
        PhoneNumberFactory.create_batch(4)
        AddressFactory.create_batch(4)

        physical_persons = PhysicalPersonFactory.create_batch(2)
        companies = CompanyFactory.create_batch(4)

        CustomUserFactory.create_batch(2, personal=factory.Iterator(physical_persons))
        CustomUserFactory.create_batch(4, is_company=True, company=factory.Iterator(companies))

        def create_related_objects():
            category = CategoryFactory()
            category.save()
            product = ProductFactory(category=category)
            product.save()

            ImageFactory(product=product)
            return product

        [create_related_objects() for _ in range(10)]

        self.stdout.write(self.style.SUCCESS(_("Test data created successfully!")))
