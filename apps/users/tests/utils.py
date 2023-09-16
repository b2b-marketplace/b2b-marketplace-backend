invalid_data_for_company_account_inn_ogrn = [
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "20only_twenty_digits",
                "inn": "1234567890",
                "ogrn": "1234567890123",
                "vat": True,
                "description": "valid-description",
            },
        },
        ("`company_account` - должен состоять из 20 цифр."),
    ),
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "12345678901234567890",
                "inn": "only_10_di",
                "ogrn": "1234567890123",
                "vat": True,
                "description": "valid-description",
            },
        },
        ("`inn` - должен состоять из 10 цифр."),
    ),
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "20only_twenty_digits",
                "inn": "1234567890",
                "ogrn": "only_13_digit",
                "vat": True,
                "description": "valid-description",
            },
        },
        ("`ogrn` - должен состоять из 13 цифр."),
    ),
]

request_valid_data = {
    "email": "validemail@mail.fake",
    "username": "valid-username",
    "password": "12345678",
    "company": {
        "role": "customer",
        "name": "valid-name",
        "inn": "1010101010",
        "address": {"address": "earth"},
        "phone_number": {"phone_number": "123"},
        "vat": True,
        "description": "description",
    },
}

response_valid_data_company_registration = {
    "id": 1,
    "email": "validemail@mail.fake",
    "is_company": True,
    "company": {
        "id": 1,
        "role": "customer",
        "name": "valid-name",
        "inn": "1010101010",
        "ogrn": None,
        "address": {"id": 1, "address": "earth"},
        "phone_number": {"id": 1, "phone_number": "123"},
        "vat": True,
        "description": "description",
    },
}
