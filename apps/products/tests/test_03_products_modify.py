import pytest
from rest_framework import status

PRODUCTS_ENDPOINT = "/api/v1/products/"

PRODUCT_RESPONSE = {
    "id": 11,
    "seller": {"id": 2, "name": "OOO Название"},
    "category": {"id": 1, "name": "Категория-1", "slug": "kategoriya-1", "parent_id": 3},
    "sku": "789",
    "name": "789",
    "brand": "Some brand",
    "price": "789.00",
    "wholesale_quantity": 789,
    "video": "http://host.ru/media/products/kategoriya-1/789/video.mp4",
    "quantity_in_stock": 789,
    "description": "Some description",
    "manufacturer_country": "China",
    "images": [{"image": "http://host.ru/media/products/kategoriya-1/789/image.bmp"}],
    "is_favorited": "false",
}


PRODUCT_CREATE_REQUEST = {
    "sku": "789",
    "name": "789",
    "brand": "Some brand",
    "price": "789.00",
    "wholesale_quantity": 789,
    "quantity_in_stock": 789,
    "description": "Some description",
    "manufacturer_country": "China",
    "images": [{"image": "http://host.ru/media/products/kategoriya-1/789/image.bmp"}],
}

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
