import pytest
from rest_framework.test import APIClient

from apps.users.models import Address, Company, PhoneNumber


@pytest.fixture
def apiclient():
    return APIClient()


@pytest.fixture
def company(django_user_model):
    phone_number = PhoneNumber.objects.create(phone_number="1234567")
    address = Address.objects.create(address="earth")
    company_obj = Company.objects.create(
        role="supplier",
        name="best_company",
        company_account="12345678901234567890",
        inn="1234567890",
        ogrn="1234567890123",
        phone_number=phone_number,
        address=address,
    )
    return django_user_model.objects.create_user(
        email="company@company.fake",
        username="companyuser",
        password="12345678",
        is_company=True,
        company=company_obj,
    )


@pytest.fixture
def company_client(company):
    client = APIClient()
    client.force_authenticate(user=company)
    return client
