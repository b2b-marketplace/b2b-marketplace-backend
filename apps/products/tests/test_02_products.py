import pytest
from rest_framework import status

PRODUCTS_ENDPOINT = "/api/v1/products/"

PRODUCT_RESPONSE = {
    "id": 11,
    "seller": {"id": 2, "name": "OOO Название"},
    "category": {"id": 1, "name": "Категория-1", "slug": "kategoriya-1", "parent_id": 3},
    "sku": "789",
    "name": "789",
    "brand": "789",
    "price": "789.00",
    "wholesale_quantity": 789,
    "videos": [{"video": "http://host.ru/media/products/kategoriya-1/789/video.mp4"}],
    "quantity_in_stock": 789,
    "description": "789",
    "manufacturer_country": "789",
    "images": [{"image": "http://host.ru/media/products/kategoriya-1/789/image.bmp"}],
}


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


# TODO: создание/обновление/удаление не разрешено гостю.
# Переписать и дополнить тесты после того, как будет реализована аутентификаиции.
def test_create_product_smoke(guest_client):
    response = guest_client.post(PRODUCTS_ENDPOINT)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


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
