import pytest

from apps.products.models import Category


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
def categories():
    cat1 = Category.objects.create(name="Товары для дома", slug="tovary-dlya-doma")
    Category.objects.create(name="Посуда", slug="posuda", parent=cat1)
    Category.objects.create(name="Бытовая химия", slug="bytovaya-khimiya", parent=cat1)
    return Category.objects.all()
