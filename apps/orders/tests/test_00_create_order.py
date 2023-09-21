from unittest import mock

import pytest
from rest_framework import status

from apps.orders.tests.conftest import mock_time_now
from apps.orders.tests.utils import response_order


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Test00OrderAPI:
    orders_url = "/api/v1/orders/"

    @mock.patch("django.utils.timezone.now", mock_time_now)
    def test_00_create_order(self, guest_client, auth_client, product_1, basket):
        order_data = {
            "order_products": [
                {
                    "product": 1,
                    "quantity": 3,
                },
                {
                    "product": 2,
                    "quantity": 5,
                },
            ]
        }

        response = guest_client.post(self.orders_url, data=order_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        assert basket.basket_products.count() == 2

        response = auth_client.post(self.orders_url, data=order_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.json()) == 2
        assert basket.basket_products.count() == 0

        assert response.json() == response_order

    def test_00_delete_order(self, guest_client, auth_client, order_1):
        response = guest_client.delete(f"{self.orders_url}{1}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = auth_client.delete(f"{self.orders_url}{1}/")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code == status.HTTP_204_NO_CONTENT
