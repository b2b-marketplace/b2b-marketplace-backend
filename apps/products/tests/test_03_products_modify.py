import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from apps.products.models import Product
from apps.products.tests.utils import (
    INVALID_PRODUCT_CREATE_REQUEST,
    PRODUCT_CREATE_REQUEST,
)

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


@pytest.mark.parametrize("payload", [{}, INVALID_PRODUCT_CREATE_REQUEST])
def test_create_product_not_allowed_with_empty_or_invalid_data(authorized_seller, payload):
    response = authorized_seller.post(PRODUCTS_ENDPOINT, payload)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    for field in set(PRODUCT_CREATE_REQUEST):
        assert field in response_data
    assert Product.objects.all().count() == 0


def test_create_product_invalid_content_type(authorized_seller):
    response = authorized_seller.post(PRODUCTS_ENDPOINT, PRODUCT_CREATE_REQUEST, format="json")
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


def test_create_product_with_valid_data_without_media(authorized_seller, categories):
    payload = PRODUCT_CREATE_REQUEST
    payload.update(category=categories[0].pk)
    response = authorized_seller.post(PRODUCTS_ENDPOINT, payload)
    db_products = Product.objects.all()
    assert db_products.count() == 1

    assert response.status_code == status.HTTP_201_CREATED

    json_data = response.json()
    assert db_products[0].name == json_data.get("name") == PRODUCT_CREATE_REQUEST.get("name")


def test_create_product_with_valid_images(authorized_seller, categories, valid_images):
    payload = PRODUCT_CREATE_REQUEST
    images = valid_images(5)
    payload.update(images=images)
    payload.update(category=categories[0].pk)
    response = authorized_seller.post(PRODUCTS_ENDPOINT, payload)
    assert response.status_code == status.HTTP_201_CREATED

    db_products = Product.objects.all()
    assert db_products.count() == 1

    response_data = response.json()
    assert db_products[0].name == response_data.get("name") == PRODUCT_CREATE_REQUEST.get("name")
    assert len(response_data.get("images")) == len(images)


def test_create_product_not_allowed_with_more_than_5_images(
    authorized_seller, categories, valid_images
):
    payload = PRODUCT_CREATE_REQUEST
    payload.update(images=valid_images(6))
    payload.update(category=categories[0].pk)
    response = authorized_seller.post(PRODUCTS_ENDPOINT, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "images" in response.json()
    assert Product.objects.all().count() == 0


@pytest.mark.parametrize("media_type", ["images", "videos"])
def test_create_product_not_allowed_with_invalid_images_or_video(authorized_seller, media_type):
    payload = PRODUCT_CREATE_REQUEST
    payload.update(
        {
            media_type: [
                SimpleUploadedFile(
                    name="invalid_media_file.txt",
                    content=b"some invalid content",
                    content_type="text/html",
                )
            ]
        }
    )
    response = authorized_seller.post(PRODUCTS_ENDPOINT, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert media_type in response.json()


def test_update_product_not_allowed_for_guest(guest_client, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = guest_client.patch(endpoint, {"some": "data"})
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_product_allowed_for_owner(authorized_seller, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = authorized_seller.patch(endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_delete_product_not_allowed_for_guest(guest_client, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = guest_client.delete(endpoint)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_product_allowed_for_owner(authorized_seller, product):
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = authorized_seller.delete(endpoint)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_product_does_not_remove_entry_from_database(authorized_seller, product):
    product_count = Product.objects.all().count()
    endpoint = f"{PRODUCTS_ENDPOINT}{product[0].pk}/"
    response = authorized_seller.delete(endpoint)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.all().count() == product_count
