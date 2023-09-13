import pytest
from django.core import mail
from rest_framework import status

from apps.users.tests.utils import (
    invalid_data_for_company_account_inn_ogrn,
    request_valid_data,
    response_valid_data_company_registration,
)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Test00CompanyRegistration:
    url_signup = "/api/v1/users/companies/"
    activate_url = "/api/v1/users/activation/"
    login_url = "/api/v1/auth/token/login/"
    user_me_url = "/api/v1/users/me/"

    def test_00_nodata_signup(self, apiclient):
        response = apiclient.post(self.url_signup, format="json")

        assert response.status_code != status.HTTP_404_NOT_FOUND

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response_json = response.json()
        empty_fields = ["email", "username", "company"]
        for field in empty_fields:
            assert field in response_json and isinstance(response_json.get(field), list)

    def test_00_invalid_data_signup(self, apiclient, django_user_model):
        invalid_data = {
            "email": "invalid_email",
            "username": " ",
            "company": {
                "role": "customer",
                "name": " ",
                "company_account": "20only_twenty_digits",
                "inn": "only_10_di",
                "ogrn": "only_13_digit",
                "address": {"address": "address"},
                "phone_number": {"phone_number": "1234567"},
                "vat": "yes",
            },
        }

        users_count = django_user_model.objects.count()
        response = apiclient.post(self.url_signup, data=invalid_data, format="json")

        assert response.status_code != status.HTTP_404_NOT_FOUND

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert users_count == django_user_model.objects.count()

    @pytest.mark.parametrize("data,message", invalid_data_for_company_account_inn_ogrn)
    def test_00_signup_length_and_simbols_validation(
        self, apiclient, data, message, django_user_model
    ):
        users_count = django_user_model.objects.count()
        response = apiclient.post(self.url_signup, data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST, message

        assert users_count == django_user_model.objects.count()

    def test_00_valid_data_company_signup(self, apiclient, django_user_model):
        outbox_before_count = len(mail.outbox)

        response = apiclient.post(self.url_signup, data=request_valid_data, format="json")
        outbox_after = mail.outbox

        assert response.status_code != status.HTTP_404_NOT_FOUND
        # import pdb; pdb.set_trace()
        assert response.status_code == status.HTTP_201_CREATED

        assert response.json() == response_valid_data_company_registration

        new_user = django_user_model.objects.filter(
            email=response_valid_data_company_registration["email"]
        )
        assert new_user.exists()

        assert len(outbox_after) == outbox_before_count + 1

        new_user.delete()

    def test_00_01_valid_data_company_signup_activation(self, apiclient):
        response = apiclient.post(self.url_signup, data=request_valid_data, format="json")
        assert len(mail.outbox) == 1

        email_lines = mail.outbox[0].body.splitlines()
        activation_link = [line for line in email_lines if "/activate/" in line][0]
        uid, token = activation_link.split("/")[-2:]
        data = {"uid": uid, "token": token}

        response = apiclient.post(self.activate_url, data=data, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        login_data = {
            "email": "validemail@mail.fake",
            "password": "Grv&blj11765",
        }

        response = apiclient.post(self.login_url, data=login_data, format="json")
        assert "auth_token" in response.json()

        token = response.json()["auth_token"]

        response = apiclient.get(self.user_me_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        apiclient.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        response = apiclient.get(self.user_me_url)
        assert response.status_code == status.HTTP_200_OK

    def test_00_registration_me_username_restricted(self, apiclient):
        valid_data = {
            "email": "validemail@mail.fake",
            "username": "me",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "12345678901234567890",
                "inn": "1234567890",
                "ogrn": "1234567890123",
                "address": {"address": "address"},
                "phone_number": {"phone_number": "+79051234560"},
                "vat": True,
            },
        }
        response = apiclient.post(self.url_signup, data=valid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
