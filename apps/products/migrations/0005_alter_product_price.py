# Generated by Django 4.1 on 2023-09-07 17:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_remove_product_video_video"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=11,
                validators=[django.core.validators.MinValueValidator(0.01)],
                verbose_name="Product price",
            ),
        ),
    ]