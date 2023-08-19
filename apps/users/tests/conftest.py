import pytest
from rest_framework.test import APIClient


@pytest.fixture
def apiclient():
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
            "address": {"address": "address"},
            "phone_number": {"phone_number": "1234567"},
        },
    }
    user = django_user_model.objects.create_user(**data)
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def company_client(company):
    client = APIClient()
    client.force_authenticate(user=company)
    return client


@pytest.fixture
def customer_company(django_user_model):
    data = {
        "email": "customer@company.fake",
        "username": "customer-company",
        "password": "12345678",
        "company": {
            "role": "customer",
            "name": "customer_company",
            "inn": "1111111111",
            "ogrn": "3333333333333",
            "company_account": "22222222222222222222",
            "address": {"address": "address"},
            "phone_number": {"phone_number": "123456789"},
        },
    }
    user = django_user_model.objects.create_user(**data)
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def customer_company_client(customer_company):
    client = APIClient()
    client.force_authenticate(user=customer_company)
    return client

