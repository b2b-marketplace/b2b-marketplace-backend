import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_username(value):
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
    if len(value) != expected_length:
        raise ValidationError(error_message)


def validate_account(value):
    validate_length(value, 20, _("The account number must contain exactly 20 characters."))


def validate_inn(value):
    validate_length(value, 10, _("The TIN must contain exactly 10 characters."))


def validate_ogrn(value):
    validate_length(value, 13, _("The PSRN must contain exactly 13 characters."))


def validate_digits_only(value):
    if not value.isdigit():
        raise ValidationError(_("Only digits are allowed."))


def validate_phone_number(value):
    pattern = r"^\+?[0-9]*$"
    if not re.match(pattern, value):
        raise ValidationError(_("Invalid phone number format"))


class PhoneNumber(models.Model):
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_phone_number],
        verbose_name=_("Phone number"),
    )

    def __str__(self):
        return self.phone_number


class Address(models.Model):
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.address


class Company(models.Model):
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


class CustomUser(AbstractUser):
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

    class Meta:
        swappable = "AUTH_USER_MODEL"
        ordering = ("username",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        if self.is_company and not self.company:
            raise ValidationError(_("Company field is required for companies!"))
        if not (self.is_superuser or self.is_staff) and not (self.is_company or self.personal):
            raise ValidationError(_("Personal field is required for physical persons!"))

    def save(self, *args, **kwargs):
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
