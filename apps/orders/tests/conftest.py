import pytest
from rest_framework.test import APIClient

from apps.baskets.models import Basket, BasketProduct
from apps.orders.models import Order, OrderProduct
from apps.products.models import Category, Image, Product
from apps.users.models import CustomUser, PhysicalPerson


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
    personal = PhysicalPerson.objects.create(first_name="person", last_name="person")
    return CustomUser.objects.create(username="username", personal=personal)


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
def product_1(company, categories):
    product = Product.objects.create(
        user=company,
        category=categories[0],
        sku="123",
        name="product_1",
        brand="product_1",
        price=500,
        wholesale_quantity=1000,
        video="path/to/video.mp4",
        quantity_in_stock=12000,
        description="product_1",
        manufacturer_country="product_1",
    )
    Image.objects.create(product=product, image="path/to/image.jpg")
    return product


@pytest.fixture
def product_2(company, categories):
    product = Product.objects.create(
        user=company,
        category=categories[0],
        sku="123",
        name="product_2",
        brand="product_2",
        price=500,
        wholesale_quantity=1000,
        video="path/to/video.mp4",
        quantity_in_stock=12000,
        description="product_2",
        manufacturer_country="product_2",
    )
    Image.objects.create(product=product, image="path/to/image.jpg")
    return product


@pytest.fixture
def basket(user, product_1, product_2):
    basket = Basket.objects.create(user=user)
    BasketProduct.objects.create(basket=basket, product=product_1, quantity=10)
    BasketProduct.objects.create(basket=basket, product=product_2, quantity=10)
    return basket


@pytest.fixture
def order(user, product_1):
    order = Order.objects.create(user=user)
    OrderProduct.objects.create(order=order, product=product_1, quantity=3, discount=10.00)
    return order
