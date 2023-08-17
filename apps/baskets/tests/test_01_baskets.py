import pytest
from rest_framework import status

BASKETS_ENDPOINT = "/api/v1/baskets/"

pytestmark = pytest.mark.django_db


def test_create_basket(guest_client):
    response = guest_client.post(BASKETS_ENDPOINT)
    assert response.status_code == status.HTTP_201_CREATED


def test_get_basket_by_id(guest_client, basket):
    print(print(dir(basket)))
    print(basket.values_list())
    endpoint = f"{BASKETS_ENDPOINT}{basket[0].pk}/"
    response = guest_client.get(endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_delete_basket_by_id(guest_client, basket):
    endpoint = f"{BASKETS_ENDPOINT}{basket[72].pk}/"
    response = guest_client.delete(endpoint)
    assert response.status_code == status.HTTP_204_NO_CONTENT


# TODO: создание/обновление/удаление не разрешено гостю.
# Переписать и дополнить тесты после того, как будет реализована аутентификаиции.
def test_create_product_in_mine_basket_smoke(guest_client):
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = guest_client.post(endpoint)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_product_in_mine_basket_smoke(guest_client, basket, product):
    print(basket)
    print(product)
    updated_basket_data = {"basket_products": [{"id": 5, "quantity": 234}]}
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = guest_client.put(endpoint, data=updated_basket_data)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# def test_delete_product_in_mine_basket_smoke(guest_client, product):
#     endpoint = f"{BASKETS_ENDPOINT}mine/"
#     response = guest_client.put(endpoint, {"some": "data"})
#     assert response.status_code != status.HTTP_404_NOT_FOUND
#     assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_mine_basket_smoke(guest_client, basket):
    endpoint = f"{BASKETS_ENDPOINT}mine/"
    response = guest_client.get(endpoint)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_200_OK
