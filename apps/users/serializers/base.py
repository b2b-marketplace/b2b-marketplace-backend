from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """Абстрактный сериализатор для создания нового пользователя."""

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def _flatten_dict(self, validated_data: dict) -> dict:
        """Преобразует данные в плоский вид.

        {
         'email': '',
         'username': ''
         'password': '',
         'company': {},
         'address': {},
         'phone_number': {},
         }
        """
        out = {}

        def flatten(data, name=""):
            tmp = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    out[key] = flatten(value, key)
                elif isinstance(value, list):
                    out[key] = value
                else:
                    tmp[key] = value

                if name == "":
                    out.update(tmp)
            return tmp

        flatten(validated_data)
        return out
