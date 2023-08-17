import re

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    """ Валидация имени пользователя. """

    pattern = r"^[\w.@+-]+$"
    regex_pattern = re.compile(pattern)
    if not regex_pattern.match(value):
        invalid_chars = []
        for char in value:
            if not regex_pattern.match(char):
                invalid_chars.append(char)
        raise ValidationError(
            _("Invalid characters: %(invalid_chars)s") % {"invalid_chars": ", ".join(invalid_chars)}
        )
    if value.lower() == "me":
        raise ValidationError(_("Cannot use 'me' as a username!"))
    return value


def validate_length(value, expected_length, error_message):
    """ Валидация длины строки. """

    if len(value) != expected_length:
        raise ValidationError(error_message)


def validate_account(value):
    """ Валидация номера счета. """

    validate_length(value, 20, _("The account number must contain exactly 20 characters."))


def validate_inn(value):
    """ Валидация ИНН. """

    validate_length(value, 10, _("The TIN must contain exactly 10 characters."))


def validate_ogrn(value):
    """ Валидация ОГРН. """

    validate_length(value, 13, _("The PSRN must contain exactly 13 characters."))


def validate_digits_only(value):
    """ Валидация цифр. """

    if not value.isdigit():
        raise ValidationError(_("Only digits are allowed."))


def validate_phone_number(value):
    """ Валидация номера телефона. """

    pattern = r"^\+?[0-9]*$"
    if not re.match(pattern, value):
        raise ValidationError(_("Invalid phone number format"))


class PhoneNumber(models.Model):
    """Модель для хранения телефонных номеров."""

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_phone_number],
        verbose_name=_("Phone number"),
    )

    def __str__(self):
        return self.phone_number


class Address(models.Model):
    """ Модель для хранения адресов. """

    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.address


class Company(models.Model):
    """ Модель для хранения компаний. """

    ROLE_CHOICES = (
        ("supplier", "supplier"),
        ("customer", "customer"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=False, null=True)
    name = models.CharField(max_length=100)
    company_account = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_account, validate_digits_only],
        verbose_name=_("Account"),
        null=True,
        blank=True,
    )
    inn = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_inn, validate_digits_only],
        verbose_name=_("TIN"),
    )
    ogrn = models.CharField(
        max_length=13,
        unique=True,
        validators=[validate_ogrn, validate_digits_only],
        verbose_name=_("PSRN"),
        null=True,
        blank=True,
    )
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.SET_NULL, null=True, blank=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name


class PhysicalPerson(models.Model):
    """ Модель для хранения физических лиц. """

    first_name = models.CharField(max_length=150, blank=False, verbose_name=_("Name"))
    last_name = models.CharField(max_length=150, blank=False, verbose_name=_("Surname"))
    personal_account = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_account, validate_digits_only],
        verbose_name=_("Account"),
    )
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.SET_NULL, null=True, blank=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ("last_name",)
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomUserManager(UserManager):
    """  Менеджер пользователей с расширенными функциями для работы с профилями и компаниями.

    Этот менеджер расширяет функциональность стандартного менеджера пользователей (UserManager),
    предоставляя дополнительные методы для создания и обновления пользователей,
    а также работы с компаниями.
    """
    def _save_object(self, model, extra_fields):
        """ Создает и сохраняет объект указанной модели с дополнительными полями. """

        obj = model()
        for key, value in extra_fields.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def _profile(self, field_name, model, extra_fields, instance=None):
        """ Создает и обновляет профиль пользователя с дополнительными полями. """

        address = extra_fields[field_name].pop("address", None)
        phone_number = extra_fields[field_name].pop("phone_number", None)

        obj_model = getattr(instance, field_name) if instance else model
        obj = self._save_object(obj_model, extra_fields.pop(field_name, None))

        if address:
            address_model = getattr(obj_model, "address") if instance else Address
            address = self._save_object(address_model, address)
            obj.address = address

        if phone_number:
            phone_number_model = getattr(obj_model, "phone_number") if instance else PhoneNumber
            phone_number = self._save_object(phone_number_model, phone_number)
            obj.phone_number = phone_number

        obj.save()
        return obj

    def create_user(self, username, email=None, password=None, **extra_fields):
        """ Создает пользователя с расширенными полями. """

        extra_fields.setdefault("is_active", False)

        if "company" in extra_fields:
            extra_fields.setdefault("is_company", True)
            company = self._profile("company", Company, extra_fields)
            extra_fields.setdefault("company", company)

        return super().create_user(username, email, password, **extra_fields)

    def get_companies(self):
        """ Возвращает компании пользователя. """

        return self.filter(Q(is_company=True) & Q(is_active=True)).select_related(
            "company", "company__address", "company__phone_number"
        )


class CustomUser(AbstractUser):
    """Пользовательский класс пользователя.

        Пользовательский класс, основанный на AbstractUser с дополнительными полями.
    """
    email = models.EmailField(unique=True, blank=False, max_length=254, verbose_name=_("Email"))
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[validate_username],
        verbose_name=_("Username"),
    )

    is_company = models.BooleanField(default=False)
    company = models.OneToOneField(
        Company,
        related_name="company_user",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    personal = models.OneToOneField(
        PhysicalPerson,
        related_name="personal_user",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = CustomUserManager()

    class Meta:
        swappable = "AUTH_USER_MODEL"
        ordering = ("username",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        """ Проверка полей при сохранении модели. """

        super().clean()
        if self.is_company and not self.company:
            raise ValidationError(_("Company field is required for companies!"))
        if not (self.is_superuser or self.is_staff) and not (self.is_company or self.personal):
            raise ValidationError(_("Personal field is required for physical persons!"))

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения объекта.

        Если пользователь является суперпользователем или персоналом,
        сбрасываем поле 'role' и устанавливаем 'is_company' в False.

        Если пользователь не является компанией, сбрасываем поле 'company'.

        Если пользователь является компанией, сбрасываем поле 'personal'.
        """
        if self.is_superuser or self.is_staff:
            self.role = None
            self.is_company = False
        if not self.is_company:
            self.company = None
        if self.is_company:
            self.personal = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def delete(self):
        """Предотвращает удаление модели.

        Вместо непосредственного удаления, помечает запись удалённой (is_active=True).
        """
        self.is_active = False
        self.save()
