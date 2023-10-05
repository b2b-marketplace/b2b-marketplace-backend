import pytest
from rest_framework.test import APIClient

from apps.baskets.models import Basket, BasketProduct
from apps.deliveries.models import Delivery, DeliveryMethod
from apps.orders.models import Order, OrderProduct
from apps.products.models import Category, Image, Product
from apps.users.models import Address, CustomUser, PhysicalPerson


def mock_time_now():
    return "2023-07-24"


@pytest.fixture
def guest_client():
    return APIClient()


@pytest.fixture
def seller_1(django_user_model):
    data = {
        "email": "seller_1@seller_1.fake",
        "username": "seller_1",
        "password": "12345678",
        "company": {
            "role": "supplier",
            "name": "seller_1",
            "inn": "1" * 10,
            "ogrn": "1" * 13,
            "company_account": "1" * 20,
        },
    }
    user = django_user_model.objects.create_user(**data)
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def seller_2(django_user_model):
    data = {
        "email": "seller_2@seller_2.fake",
        "username": "seller_2",
        "password": "12345678",
        "company": {
            "role": "supplier",
            "name": "seller_2",
            "inn": "2" * 10,
            "ogrn": "2" * 13,
            "company_account": "2" * 20,
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
def auth_seller_1(seller_1):
    client = APIClient()
    client.force_authenticate(user=seller_1)
    return client


@pytest.fixture
def auth_seller_2(seller_2):
    client = APIClient()
    client.force_authenticate(user=seller_2)
    return client


@pytest.fixture
def categories():
    cat1 = Category.objects.create(name="Товары для дома", slug="tovary-dlya-doma")
    Category.objects.create(name="Посуда", slug="posuda", parent=cat1)
    Category.objects.create(name="Бытовая химия", slug="bytovaya-khimiya", parent=cat1)
    return Category.objects.all()


@pytest.fixture
def product_1(seller_1, categories):
    product = Product.objects.create(
        user=seller_1,
        category=categories[0],
        sku="123",
        name="product_1",
        brand="product_1",
        price=500,
        wholesale_quantity=1000,
        quantity_in_stock=12000,
        description="product_1",
        manufacturer_country="product_1",
    )
    Image.objects.create(product=product, image="path/to/image.jpg")
    return product


@pytest.fixture
def product_2(seller_2, categories):
    product = Product.objects.create(
        user=seller_2,
        category=categories[0],
        sku="123",
        name="product_2",
        brand="product_2",
        price=500,
        wholesale_quantity=1000,
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
def delivery_method():
    delivery_method = DeliveryMethod.objects.create(
        name="DHL",
        description="DHL delivery",
        slug="dhl",
        price=1000,
    )
    return delivery_method


@pytest.fixture
def address():
    address = Address.objects.create(address="address")
    return address


@pytest.fixture
def order_1(user, product_1, delivery_method, address):
    order = Order.objects.create(user=user)

    OrderProduct.objects.create(order=order, product=product_1, quantity=3, price=100)
    return order


@pytest.fixture
def delivery_1(order_1, address, delivery_method):
    delivery = Delivery.objects.create(
        order=order_1,
        address=address,
        delivery_method=delivery_method,
        delivery_date="2023-10-04T12:38:14.540Z",
    )
    return delivery


@pytest.fixture
def order_2(user, product_2):
    order = Order.objects.create(user=user)
    OrderProduct.objects.create(order=order, product=product_2, quantity=3, price=100)
    return order


@pytest.fixture
def delivery_2(order_2, address, delivery_method):
    delivery = Delivery.objects.create(
        order=order_2,
        address=address,
        delivery_method=delivery_method,
        delivery_date="2023-10-04T12:38:14.540Z",
    )
    return delivery
