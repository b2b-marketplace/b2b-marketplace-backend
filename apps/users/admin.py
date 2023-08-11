from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, Company, CustomUser, PhoneNumber, PhysicalPerson


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Role Info", {"fields": ("role", "is_company", "company", "personal")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
        (
            "Role Info",
            {
                "classes": ("wide",),
                "fields": ("role", "is_company", "company", "personal"),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("wide",),
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "role",
        "is_company",
    )
    list_filter = (
        "role",
        "is_company",
    )
    empty_value_display = "-empty-"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    empty_value_display = "-empty-"


@admin.register(PhysicalPerson)
class PhysicalPersonAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
    )
    empty_value_display = "-empty-"


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("phone_number",)
    empty_value_display = "-empty-"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address",)
    empty_value_display = "-empty-"
