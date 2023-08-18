import pytest
from rest_framework import status

BASKETS_ENDPOINT = "/api/v1/baskets/"

pytestmark = pytest.mark.django_db


def test_create_basket(auth_client, user):
    response = auth_client.post(BASKETS_ENDPOINT)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert "id" in data
    assert "user" in data
    assert data["user"] == user.id
    assert "basket_products" in data
    assert len(data["basket_products"]) == 0


def test_get_basket_by_id(auth_client, basket, user):
    endpoint = f"{BASKETS_ENDPOINT}{basket[0].pk}/"
    response = auth_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_delete_basket_by_id(auth_client, basket, user):
    endpoint = f"{BASKETS_ENDPOINT}{basket[0].pk}/"
    response = auth_client.delete(endpoint)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = auth_client.get(endpoint)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_product_in_mine_basket(auth_client, product, user):
    basket_data = {"basket_products": [{"id": product[0].id, "quantity": 200}]}
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = auth_client.post(endpoint, basket_data, format="json")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "basket_products" in data
    assert len(data["basket_products"]) == 1

    created_product = data["basket_products"][0]
    assert created_product["product"]["id"] == product[0].id
    assert created_product["quantity"] == 200


def test_update_product_in_mine_basket(auth_client, basket, product, user):
    updated_quantity = 100
    updated_basket_data = {"basket_products": [{"id": product[0].id, "quantity": updated_quantity}]}
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = auth_client.put(endpoint, updated_basket_data, format="json")
    assert response.status_code == status.HTTP_200_OK

    response = auth_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "basket_products" in data
    updated_product = data["basket_products"][0]
    assert updated_product["quantity"] == updated_quantity


def test_delete_product_in_mine_basket(auth_client, basket, product, user):
    updated_basket_data = {"basket_products": []}
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = auth_client.put(endpoint, updated_basket_data, format="json")
    assert response.status_code == status.HTTP_200_OK

    response = auth_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "basket_products" in data
    assert len(data["basket_products"]) == 0


def test_get_mine_basket(auth_client, basket, user):
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = auth_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK
