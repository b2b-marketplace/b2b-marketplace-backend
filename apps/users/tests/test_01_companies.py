import pytest
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class Test01CompanyAPI:
    companies_url = "/api/v1/users/companies/"
    user_me_url = "/api/v1/users/me/"

    def test_01_users_get_paginated_companies(self, apiclient, company):
        response = apiclient.get(self.companies_url)

        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        expected_keys = ("count", "next", "previous", "results")

        for company in data["results"]:
            assert company["is_company"] is True

        for key in expected_keys:
            assert key in data

        assert data["count"] == 1

    def test_01_user_delete(self, apiclient, company_client, company):
        response = apiclient.delete(self.user_me_url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        login_data = {
            "current_password": "12345678",
        }

        assert company.is_active is True

        response = company_client.delete(self.user_me_url, data=login_data, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert company.is_active is False
