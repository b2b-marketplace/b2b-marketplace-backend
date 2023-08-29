import pytest

from apps.products.models import Category, Image, Product
from apps.users.models import Address, Company, CustomUser, PhoneNumber, PhysicalPerson


@pytest.fixture
def guest_client():
    """Создает клиент без авторизации."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authorized_seller(user_seller):
    from rest_framework.test import APIClient

    client = APIClient()
    client.force_authenticate(user=user_seller)
    return client


@pytest.fixture
def authorized_buyer(user_buyer):
    from rest_framework.test import APIClient

    client = APIClient()
    client.force_authenticate(user=user_buyer)
    return client


@pytest.fixture
def authorized_physical_person(user_physical_person):
    from rest_framework.test import APIClient

    client = APIClient()
    client.force_authenticate(user=user_physical_person)
    return client


@pytest.fixture
def company_seller():
    return Company.objects.create(
        role="supplier",
        name="ООО Продавец",
        company_account=12345678901234567890,
        inn=1234567890,
        ogrn=1234567890123,
        phone_number=PhoneNumber.objects.create(phone_number="+7999123456"),
        address=Address.objects.create(address="г.Важный, ул. Неважная, дом 56"),
    )


@pytest.fixture
def company_buyer():
    return Company.objects.create(
        role="customer",
        name="ПАО Покупатель",
        company_account=22345678901234567890,
        inn=2234567890,
        ogrn=2234567890123,
        phone_number=PhoneNumber.objects.create(phone_number="+7999223456"),
        address=Address.objects.create(address="г.Странный, ул. Загадочная, дом 88"),
    )


@pytest.fixture
def physical_person():
    return PhysicalPerson.objects.create(
        first_name="Вася",
        last_name="Халявщиков",
        personal_account=33345678901234567890,
        phone_number=PhoneNumber.objects.create(phone_number="+7888223456"),
        address=Address.objects.create(address="г.Потерянный, ул. Найденная, дом 123"),
    )


@pytest.fixture
def user_seller(company_seller):
    """Создает пользователя."""
    return CustomUser.objects.create(
        username="seller", email="seller@mail.ru", is_company=True, company=company_seller
    )


@pytest.fixture
def user_buyer(company_buyer):
    """Создает пользователя."""
    return CustomUser.objects.create(
        username="buyer", email="buyer@mail.ru", is_company=True, company=company_buyer
    )


@pytest.fixture
def user_physical_person(physical_person):
    """Создает пользователя."""
    return CustomUser.objects.create(
        username="physical",
        email="physical@mail.ru",
        is_company=False,
        personal=physical_person,
    )


@pytest.fixture
def categories():
    """Создает категории."""
    cat1 = Category.objects.create(name="Товары для дома", slug="tovary-dlya-doma")
    Category.objects.create(name="Посуда", slug="posuda", parent=cat1)
    Category.objects.create(name="Бытовая химия", slug="bytovaya-khimiya", parent=cat1)
    return Category.objects.all()


@pytest.fixture
def product(user_seller, categories):
    """Создает продукт."""
    product = Product.objects.create(
        user=user_seller,
        category=categories[0],
        sku="123",
        name="Майка",
        brand="Ультра майки инкорпорейтед",
        price="500",
        wholesale_quantity="1000",
        video="path/to/video.mp4",
        quantity_in_stock="12000",
        description="Майка как майка",
        manufacturer_country="Китай",
    )
    Image.objects.create(product=product, image="path/to/image.jpg")
    return Product.objects.all()
