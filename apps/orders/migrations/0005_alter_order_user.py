# Generated by Django 4.1 on 2023-08-27 16:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.orders.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0004_alter_orderproduct_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="customer",
                to=settings.AUTH_USER_MODEL,
                validators=[apps.orders.models.validate_user_is_buyer],
                verbose_name="Order owner",
            ),
        ),
    ]
