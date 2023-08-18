import pytest
from rest_framework import status

BASKETS_ENDPOINT = "/api/v1/baskets/"

pytestmark = pytest.mark.django_db


def test_create_basket(guest_client, user):
    response = guest_client.post(BASKETS_ENDPOINT)
    assert response.status_code == status.HTTP_201_CREATED
    # assert response.status_code != status.HTTP_400_BAD_REQUEST
    # assert response.status_code != status.HTTP_401_UNAUTHORIZED
    # assert response.status_code != status.HTTP_403_FORBIDDEN


def test_get_basket_by_id(guest_client, basket, user):
    endpoint = f"{BASKETS_ENDPOINT}{basket[0].pk}/"
    response = guest_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK
    # assert response.status_code != status.HTTP_401_UNAUTHORIZED
    # assert response.status_code != status.HTTP_403_FORBIDDEN
    # assert response.status_code != status.HTTP_404_NOT_FOUND


def test_delete_basket_by_id(guest_client, basket, user):
    endpoint = f"{BASKETS_ENDPOINT}{basket[0].pk}/"
    response = guest_client.delete(endpoint)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # assert response.status_code != status.HTTP_400_BAD_REQUEST
    # assert response.status_code != status.HTTP_401_UNAUTHORIZED
    # assert response.status_code != status.HTTP_403_FORBIDDEN
    # assert response.status_code != status.HTTP_404_NOT_FOUND

    response = guest_client.get(endpoint)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO: создание/обновление/удаление не разрешено гостю.
# Переписать и дополнить тесты после того, как будет реализована аутентификаиции.
def test_create_product_in_mine_basket(guest_client, product, user):
    basket_data = {"basket_products": [{"id": product[0].id, "quantity": 200}]}
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = guest_client.post(endpoint, basket_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    # assert response.status_code != status.HTTP_400_BAD_REQUEST
    # assert response.status_code != status.HTTP_401_UNAUTHORIZED
    # assert response.status_code != status.HTTP_403_FORBIDDEN
    # assert response.status_code != status.HTTP_404_NOT_FOUND

    data = response.json()
    assert "basket_products" in data
    assert len(data["basket_products"]) == 1

    created_product = data["basket_products"][0]
    assert created_product["product"]["id"] == product[0].id
    assert created_product["quantity"] == 200


def test_update_product_in_mine_basket(guest_client, basket, product, user):
    updated_quantity = 100
    updated_basket_data = {"basket_products": [{"id": product[0].id, "quantity": updated_quantity}]}
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = guest_client.put(endpoint, updated_basket_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    # assert response.status_code != status.HTTP_400_BAD_REQUEST
    # assert response.status_code != status.HTTP_401_UNAUTHORIZED
    # assert response.status_code != status.HTTP_403_FORBIDDEN
    # assert response.status_code != status.HTTP_404_NOT_FOUND

    response = guest_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "basket_products" in data
    updated_product = data["basket_products"][0]
    assert updated_product["quantity"] == updated_quantity


def test_delete_product_in_mine_basket(guest_client, basket, product, user):
    updated_basket_data = {"basket_products": []}
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = guest_client.put(endpoint, updated_basket_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    # assert response.status_code != status.HTTP_400_BAD_REQUEST
    # assert response.status_code != status.HTTP_401_UNAUTHORIZED
    # assert response.status_code != status.HTTP_403_FORBIDDEN
    # assert response.status_code != status.HTTP_404_NOT_FOUND

    response = guest_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "basket_products" in data
    assert len(data["basket_products"]) == 0


def test_get_mine_basket(guest_client, basket, user):
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = guest_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK
    # assert response.status_code != status.HTTP_401_UNAUTHORIZED
    # assert response.status_code != status.HTTP_403_FORBIDDEN
    # assert response.status_code != status.HTTP_404_NOT_FOUND
