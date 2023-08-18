from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat


MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 Мб


@deconstructible
class VideoValidator(object):
    """Валидация видеофайла."""

    error_messages = {
        "max_size": "Загружаемый файл слишком большой. Максимальный размер: %(max_size)s",
    }

    def __init__(self, max_size=MAX_VIDEO_SIZE):
        self.max_size = max_size

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                "max_size": filesizeformat(self.max_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages["max_size"], "max_size", params)


validate_video = VideoValidator(max_size=MAX_VIDEO_SIZE)
