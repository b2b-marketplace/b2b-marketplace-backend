import pytest
from rest_framework.test import APIClient

from apps.orders.models import Order, OrderProduct
from apps.products.models import Category, Image, Product
from apps.users.models import CustomUser


def mock_time_now():
    return "2023-07-24"


@pytest.fixture
def guest_client():
    return APIClient()


@pytest.fixture
def company(django_user_model):
    data = {
        "email": "company@company.fake",
        "username": "companyuser",
        "password": "12345678",
        "company": {
            "role": "supplier",
            "name": "best_company",
            "inn": "1234567890",
            "ogrn": "1234567890123",
            "company_account": "12345678901234567890",
        },
    }
    user = django_user_model.objects.create_user(**data)
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def user():
    """Создает пользователя."""
    return CustomUser.objects.create(username="username")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def categories():
    cat1 = Category.objects.create(name="Товары для дома", slug="tovary-dlya-doma")
    Category.objects.create(name="Посуда", slug="posuda", parent=cat1)
    Category.objects.create(name="Бытовая химия", slug="bytovaya-khimiya", parent=cat1)
    return Category.objects.all()


@pytest.fixture
def product(company, categories):
    product = Product.objects.create(
        user=company,
        category=categories[0],
        sku="123",
        name="Майка",
        brand="Ультра майки инкорпорейтед",
        price=500,
        wholesale_quantity=1000,
        video="path/to/video.mp4",
        quantity_in_stock=12000,
        description="Майка как майка",
        manufacturer_country="Китай",
    )
    Image.objects.create(product=product, image="path/to/image.jpg")
    return product


@pytest.fixture
def order(user, product):
    order = Order.objects.create(
        user=user,
    )
    OrderProduct.objects.create(order=order, product=product, quantity=3, discount=10.00)
    return order
