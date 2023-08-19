import magic

# TODO Необходимо на сервере установить libmagic. На Ubuntu 20.04 sudo apt-get install libmagic-dev

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat

MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 Мб
CONTENT_TYPES = (
    "video/mp4",
    "video/webm",
)


@deconstructible
class VideoValidator(object):
    """Валидация видеофайла."""

    error_messages = {
        "max_size": (
            "Загружаемый файл слишком большой. Максимальный размер: %(max_size)s. "
            "Размер загружаемого файла: %(size)s"
        ),
        "content_type": f"Загружаемый файл не является поддерживаемым видеофайлом. "
        f"Разрешенные типы: {', '.join(CONTENT_TYPES)}",
    }

    def __init__(self, max_size=MAX_VIDEO_SIZE, content_types=CONTENT_TYPES):
        self.max_size = max_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                "max_size": filesizeformat(self.max_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages["max_size"], "max_size", params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {"content_type": content_type}
                raise ValidationError(self.error_messages["content_type"], "content_type", params)

    def __eq__(self, other):
        return (
            isinstance(other, VideoValidator)
            and self.max_size == other.max_size
            and self.content_types == other.content_types
        )


validate_video = VideoValidator(max_size=MAX_VIDEO_SIZE, content_types=CONTENT_TYPES)
