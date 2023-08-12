# Generated by Django 4.1 on 2023-08-11 15:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CR", "Created"),
                            ("UP", "Updated"),
                            ("PA", "Paid"),
                            ("TR", "In_transit"),
                            ("CO", "Completed"),
                            ("CA", "Canceled"),
                            ("RE", "Returned"),
                        ],
                        default="CR",
                        max_length=2,
                        verbose_name="Order status",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="customer",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Order owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(verbose_name="Product quantity in order"),
                ),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="Product discount"
                    ),
                ),
                (
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="orders",
                        to="orders.order",
                        verbose_name="Order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="orders",
                        to="products.product",
                        verbose_name="Product in order",
                    ),
                ),
            ],
            options={
                "verbose_name": "OrderProduct",
                "verbose_name_plural": "OrderProducts",
            },
        ),
        migrations.AddIndex(
            model_name="orderproduct",
            index=models.Index(fields=["order"], name="orders_orde_order_i_d30f9b_idx"),
        ),
        migrations.AddConstraint(
            model_name="orderproduct",
            constraint=models.UniqueConstraint(
                fields=("order", "product"),
                name="orders_orderproduct_order_product_uniq",
            ),
        ),
        migrations.AddIndex(
            model_name="order",
            index=models.Index(fields=["user"], name="orders_orde_user_id_a87c6f_idx"),
        ),
    ]
