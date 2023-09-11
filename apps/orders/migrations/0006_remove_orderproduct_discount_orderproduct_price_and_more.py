# Generated by Django 4.1 on 2023-09-01 10:43

import django.core.validators
from django.db import migrations, models


def add_price_in_order_products(apps, schema_editor):
    OrderProduct = apps.get_model('orders', 'OrderProduct')
    db_alias = schema_editor.connection.alias

    for op in OrderProduct.objects.using(db_alias).all():
        op.price = op.product.price
        op.save()


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0005_alter_order_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderproduct",
            name="discount",
        ),
        migrations.AddField(
            model_name="orderproduct",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=11,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Product price",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Created", "Created"),
                    ("Updated", "Updated"),
                    ("Paid", "Paid"),
                    ("Transit", "In_transit"),
                    ("Received", "Received"),
                    ("Canceled", "Canceled"),
                    ("Returned", "Returned"),
                ],
                default="Created",
                max_length=15,
                verbose_name="Order status",
            ),
        ),
        migrations.RunPython(add_price_in_order_products, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="orderproduct",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=11,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Product price",
            ),
        ),
    ]