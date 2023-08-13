import pytest

from apps.products.models import Category, Image, Product
from apps.users.models import CustomUser


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings

    print(settings.DATABASES)
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": settings.BASE_DIR / "db.sqlite3",
        "ATOMIC_REQUESTS": False,
    }


@pytest.fixture
def guest_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user():
    return CustomUser.objects.create(username="username")


@pytest.fixture
def categories():
    cat1 = Category.objects.create(name="Товары для дома", slug="tovary-dlya-doma")
    Category.objects.create(name="Посуда", slug="posuda", parent=cat1)
    Category.objects.create(name="Бытовая химия", slug="bytovaya-khimiya", parent=cat1)
    return Category.objects.all()


@pytest.fixture
def product(user, categories):
    product = Product.objects.create(
        user=user,
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
