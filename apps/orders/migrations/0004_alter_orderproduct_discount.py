# Generated by Django 4.1 on 2023-08-25 08:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_alter_orderproduct_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderproduct",
            name="discount",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=4,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="Product discount",
            ),
        ),
    ]
