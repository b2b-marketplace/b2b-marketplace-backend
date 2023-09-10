import pytest
from rest_framework import status


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Test01CompanyAPI:
    companies_url = "/api/v1/users/companies/"
    user_me_url = "/api/v1/users/me/"

    def test_01_users_get_paginated_companies(self, apiclient, company, customer_company):
        response = apiclient.get(self.companies_url)

        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        expected_keys = ("count", "next", "previous", "results")

        for company in data["results"]:
            assert company["is_company"] is True
            assert company["company"]["role"] == "supplier"

        for key in expected_keys:
            assert key in data

        assert data["count"] == 1

    def test_01_company_update_profile(self, apiclient, company_client):
        request_data = {
            "company": {
                "role": "supplier",
                "name": "best_company",
                "ogrn": "3333333333333",
                "company_account": "22222222222222222222",
                "address": {"address": "earth"},
                "vat": True,
            },
        }

        responses_data_after_update_profile = {
            "id": 1,
            "email": "company@company.fake",
            "username": "companyuser",
            "is_company": True,
            "company": {
                "id": 1,
                "role": "supplier",
                "name": "best_company",
                "inn": "1234567890",
                "ogrn": "3333333333333",
                "company_account": "22222222222222222222",
                "address": {"id": 1, "address": "earth"},
                "phone_number": {"id": 1, "phone_number": "1234567"},
                "vat": True,
            },
        }

        response = apiclient.patch(self.user_me_url, data=request_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = company_client.patch(self.user_me_url, data=request_data, format="json")
        assert response.status_code == status.HTTP_200_OK

        assert response.json() == responses_data_after_update_profile

    def test_01_user_delete(self, apiclient, company_client, company):
        response = apiclient.delete(self.user_me_url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        assert company.is_active is True

        response = company_client.delete(self.user_me_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert company.is_active is False
