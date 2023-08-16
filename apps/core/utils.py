def _flatten_dict(validated_data: dict) -> dict:
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
