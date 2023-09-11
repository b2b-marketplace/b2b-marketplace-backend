import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    """Валидация имени пользователя."""
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
    """Валидация длины строки."""
    if len(value) != expected_length:
        raise ValidationError(error_message)


def validate_account(value):
    """Валидация номера счета."""
    validate_length(value, 20, _("The account number must contain exactly 20 characters."))


def validate_inn(value):
    """Валидация ИНН."""
    validate_length(value, 10, _("The TIN must contain exactly 10 characters."))


def validate_ogrn(value):
    """Валидация ОГРН."""
    validate_length(value, 13, _("The PSRN must contain exactly 13 characters."))


def validate_digits_only(value):
    """Валидация цифр."""
    if not value.isdigit():
        raise ValidationError(_("Only digits are allowed."))


def validate_phone_number(value):
    """Валидация номера телефона."""
    pattern = r"^\+?[0-9]*$"
    if not re.match(pattern, value):
        raise ValidationError(_("Invalid phone number format"))


def validate_user_is_supplier(value):
    """Валидатор, который проверяет, является ли пользователь поставщиком.

    Используется при создании продукта.

    """
    user = get_object_or_404(get_user_model(), pk=value)
    if not (user.is_company and user.company.role == "supplier"):
        raise ValidationError(_("The user is not a supplier."))


def validate_user_is_buyer(value):
    """
    Валидатор, который проверяет, является ли пользователь покупателем.

    Используется при создании корзины/заказа.
    """
    user = get_object_or_404(get_user_model(), pk=value)
    if not (user.personal or user.company.role == "customer"):
        raise ValidationError(_("The user is not a buyer."))
