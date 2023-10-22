import os
from tempfile import TemporaryDirectory

from .settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB_TEST"],
        "USER": os.environ["POSTGRES_USER_TEST"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD_TEST"],
        "HOST": os.environ["POSTGRES_HOST_TEST"],
        "PORT": os.environ["POSTGRES_PORT_TEST"],
    },
}

MEDIA_ROOT = TemporaryDirectory().name
