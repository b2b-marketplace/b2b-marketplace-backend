from django.db import models


class BaseModel(models.Model):
    """Абстрактная базовая модель.

    Добавляет в дочернюю модель поля:
        - created_at: дата и время создания записи в БД
        - updated_at: дата и время обновления записи в БД
    Значения в полях created_at, updated_at обновляются автоматически.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """Миксин для реализации "мягкого удаления".

    Добавляет в модель поле is_deleted. При применении метода delete() к экзмепляру модели,
    записывает в поле is_deleted значение True.
    """

    is_deleted = models.BooleanField(default=False)

    def delete(self):
        """Предотвращает удаление модели.

        Вместо непосредственного удаления, помечает модель удалённой (is_deleted=True).
        """
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True
