import factory

from .models import Address, Company, CustomUser, PhoneNumber, PhysicalPerson


class PhoneNumberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhoneNumber

    phone_number = factory.Sequence(lambda n: f"+7{n:010d}")


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    address = factory.Faker("address")


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    role = factory.Iterator(["supplier", "customer"])
    name = factory.Faker("company")
    company_account = factory.Sequence(lambda n: f"{n:020d}")
    inn = factory.Sequence(lambda n: f"{n:010d}")
    ogrn = factory.Sequence(lambda n: f"{n:013d}")
    phone_number = factory.SubFactory(PhoneNumberFactory)
    address = factory.SubFactory(AddressFactory)


class PhysicalPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhysicalPerson

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    personal_account = factory.Sequence(lambda n: f"{n:020d}")
    phone_number = factory.SubFactory(PhoneNumberFactory)
    address = factory.SubFactory(AddressFactory)


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    is_company = False
    company = None
    personal = None

    @factory.post_generation
    def set_associated_objects(self, create, extracted, **kwargs):
        if not create:
            return
        if self.is_company:
            if extracted:
                self.company = extracted
        else:
            if extracted:
                self.personal = extracted
