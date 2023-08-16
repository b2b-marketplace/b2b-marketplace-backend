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
        },
        "address": {"address": "address"},
        "phone_number": {"phone_number": "1234567"},
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
