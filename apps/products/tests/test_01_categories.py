import pytest
from rest_framework import status

from apps.products.serializers import CategorySerializer

CATEGORIES_ENDPOINT = "/api/v1/categories/"

CATEGORY_RESPONSE_FIELDS = ["id", "name", "slug", "parent_id"]

pytestmark = pytest.mark.django_db


def test_get_all_categories(guest_client, categories):
    response = guest_client.get(CATEGORIES_ENDPOINT)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_200_OK

    # pagination
    data = response.json()
    assert "count" in data
    assert data["count"] == len(categories)
    assert "next" in data
    assert "previous" in data
    assert "results" in data

    # fields
    assert isinstance(data["results"], list)
    assert set(data["results"][0]) == set(CATEGORY_RESPONSE_FIELDS)

    # data
    serializer = CategorySerializer(categories, many=True)
    assert data["results"] == serializer.data


def test_get_category_by_id(guest_client, categories):
    endpoint = f"{CATEGORIES_ENDPOINT}{categories[0].pk}/"
    response = guest_client.get(endpoint)

    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["name"] == categories[0].name


def test_only_get_method_allowed_for_categories(guest_client, categories):
    response = guest_client.post(CATEGORIES_ENDPOINT)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = guest_client.put(CATEGORIES_ENDPOINT)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = guest_client.patch(CATEGORIES_ENDPOINT)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = guest_client.delete(CATEGORIES_ENDPOINT)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
