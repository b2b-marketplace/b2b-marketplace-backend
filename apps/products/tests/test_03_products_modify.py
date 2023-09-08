import pytest
from rest_framework import status

from apps.products.tests.utils import PRODUCT_CREATE_REQUEST

PRODUCTS_ENDPOINT = "/api/v1/products/"

pytestmark = pytest.mark.django_db


def test_create_product_not_allowed_for_guest_or_buyer_or_physical(
    guest_client, authorized_buyer, authorized_physical_person
):
    response = guest_client.post(PRODUCTS_ENDPOINT)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = authorized_buyer.post(PRODUCTS_ENDPOINT)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = authorized_physical_person.post(PRODUCTS_ENDPOINT)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_product_empty_data(authorized_seller):
    response = authorized_seller.post(PRODUCTS_ENDPOINT)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    for field in set(PRODUCT_CREATE_REQUEST):
        assert field in response_data


def test_create_product_invalid_data(authorized_seller):
    pass


# TODO
# ______
#       V
def test_update_product_smoke(guest_client, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = guest_client.put(endpoint, {"some": "data"})
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_partial_update_product_smoke(guest_client, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = guest_client.patch(endpoint, {"some": "data"})
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_product_smoke(guest_client, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = guest_client.delete(endpoint)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
