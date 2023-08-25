from unittest import mock

import pytest
from rest_framework import status

from apps.orders.tests.conftest import mock_time_now


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Test00OrderAPI:
    orders_url = f"/api/v1/users/{1}/orders/"

    order = {
        "id": 1,
        "user": 1,
        "status": "CR",
        "created_at": "2023-07-24",
        "order_products": [
            {
                "product": {
                    "id": 1,
                    "supplier": {"id": 1, "name": "best_company"},
                    "sku": "123",
                    "name": "product_1",
                    "price": "500.00",
                    "images": {"image": "/media/path/to/image.jpg"},
                },
                "quantity": 3,
                "discount": "0.00",
                "cost": 1500.0,
                "cost_with_discount": 1500.0,
            },
        ],
    }

    @mock.patch("django.utils.timezone.now", mock_time_now)
    def test_00_create_order(self, guest_client, auth_client, product_1, basket):
        order_data = {
            "order_products": [
                {
                    "product": 1,
                    "quantity": 3,
                },
            ]
        }

        response = guest_client.post(self.orders_url, data=order_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        assert basket.basket_products.count() == 2

        response = auth_client.post(self.orders_url, data=order_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self.order
        assert basket.basket_products.count() == 1

    def test_00_delete_order(self, guest_client, auth_client, order):
        response = guest_client.delete(f"{self.orders_url}{1}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = auth_client.delete(f"{self.orders_url}{1}/")
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code == status.HTTP_204_NO_CONTENT
