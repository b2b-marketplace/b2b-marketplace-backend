import pytest
from rest_framework import status

from apps.products.tests.utils import PRODUCT_RESPONSE

PRODUCTS_ENDPOINT = "/api/v1/products/"

pytestmark = pytest.mark.django_db


def test_get_all_products(guest_client, product):
    response = guest_client.get(PRODUCTS_ENDPOINT)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "count" in data
    assert data["count"] == len(product)
    assert "next" in data
    assert "previous" in data
    assert "results" in data

    assert isinstance(data["results"], list)
    assert set(data["results"][0]) == set(PRODUCT_RESPONSE)

    assert data["results"][0]["name"] == product[0].name


def test_get_product_by_id(guest_client, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = guest_client.get(endpoint)

    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["name"] == product[0].name
