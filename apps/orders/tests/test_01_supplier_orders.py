import pytest
from rest_framework import status


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Test01OrderAPI:
    orders_url = "/api/v1/supplier-orders/"

    def test_01_get_supplier_orders(self, guest_client, auth_seller_1, seller_1, order_1, order_2):
        response = guest_client.get(self.orders_url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = auth_seller_1.get(self.orders_url, format="json")
        assert response.status_code == status.HTTP_200_OK
        for order in response.json()["results"]:
            for product in order["order_products"]:
                assert product["product"]["supplier"]["id"] == seller_1.id

    def test_01_change_order_status(
        self,
        guest_client,
        auth_seller_1,
        auth_seller_2,
        seller_1,
        seller_2,
        order_1,
    ):
        order_status = {"status": "Transit"}

        response = guest_client.patch(
            f"{self.orders_url}{order_1.id}/", data=order_status, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = auth_seller_2.patch(
            f"{self.orders_url}{order_1.id}/", data=order_status, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = auth_seller_1.patch(
            f"{self.orders_url}{order_1.id}/", data=order_status, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == order_status["status"]
