invalid_data_for_company_account_inn_ogrn = [
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "password": "Grv&blj11765",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "20only_twenty_digits",
                "inn": "1234567890",
                "ogrn": "1234567890123",
                "address": {"address": "earth"},
                "phone_number": {"phone_number": "+79051234562"},
                "vat": True,
            },
        },
        ("`company_account` - должен состоять из 20 цифр."),
    ),
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "password": "Grv&blj11765",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "12345678901234567890",
                "inn": "only_10_di",
                "ogrn": "1234567890123",
                "address": {"address": "earth"},
                "phone_number": {"phone_number": "+79051234562"},
                "vat": True,
            },
        },
        ("`inn` - должен состоять из 10 цифр."),
    ),
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "password": "Grv&blj11765",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "20only_twenty_digits",
                "inn": "1234567890",
                "ogrn": "only_13_digit",
                "address": {"address": "earth"},
                "phone_number": {"phone_number": "+79051234562"},
                "vat": True,
            },
        },
        ("`ogrn` - должен состоять из 13 цифр."),
    ),
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "password": "Grv&blj11765",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "12345678901234567890",
                "inn": "1234567890",
                "ogrn": "",
                "address": {"address": "earth"},
                "phone_number": {"phone_number": "+79051234562"},
                "vat": True,
            },
        },
        ("`ogrn` - не может быть пустой строкой."),
    ),
    (
        {
            "email": "validemail@mail.fake",
            "username": "valid-username",
            "password": "Grv&blj11765",
            "company": {
                "role": "customer",
                "name": "valid-name",
                "company_account": "",
                "inn": "1234567890",
                "ogrn": "1234567890123",
                "address": {"address": "earth"},
                "phone_number": {"phone_number": "+79051234562"},
                "vat": True,
            },
        },
        ("`company_account` - не может быть пустой строкой."),
    ),
]

request_valid_data = {
    "email": "validemail@mail.fake",
    "username": "valid-username",
    "password": "Grv&blj11765",
    "company": {
        "role": "customer",
        "name": "valid-name",
        "inn": "1010101010",
        "address": {"address": "earth"},
        "phone_number": {"phone_number": "+79051234562"},
        "vat": True,
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
        "phone_number": {"id": 1, "phone_number": "+79051234562"},
        "vat": True,
    },
}
