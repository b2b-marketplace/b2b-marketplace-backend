import pytest

from apps.products.models import Category, Image, Product, Video
from apps.users.models import CustomUser


@pytest.fixture
def guest_client():
    """Создает клиент без авторизации."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user():
    """Создает пользователя."""
    return CustomUser.objects.create(username="username")


@pytest.fixture
def categories():
    """Создает категории."""
    cat1 = Category.objects.create(name="Товары для дома", slug="tovary-dlya-doma")
    Category.objects.create(name="Посуда", slug="posuda", parent=cat1)
    Category.objects.create(name="Бытовая химия", slug="bytovaya-khimiya", parent=cat1)
    return Category.objects.all()


@pytest.fixture
def product(user, categories):
    """Создает продукт."""
    product = Product.objects.create(
        user=user,
        category=categories[0],
        sku="123",
        name="Майка",
        brand="Ультра майки инкорпорейтед",
        price="500",
        wholesale_quantity="1000",
        quantity_in_stock="12000",
        description="Майка как майка",
        manufacturer_country="Китай",
    )
    Image.objects.create(product=product, image="path/to/image.jpg")
    Video.objects.create(product=product, video="path/to/video.mp4")
    return Product.objects.all()
