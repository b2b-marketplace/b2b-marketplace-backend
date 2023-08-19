# Generated by Django 4.1 on 2023-08-19 00:50

import apps.products.models
import apps.products.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_remove_product_video_video"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="video",
            options={"verbose_name": "Video", "verbose_name_plural": "Videos"},
        ),
        migrations.AlterField(
            model_name="video",
            name="video",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=apps.products.models.get_product_directory_path,
                validators=[
                    apps.products.validators.VideoValidator(
                        content_types=("video/mp4", "video/webm"), max_size=104857600
                    )
                ],
                verbose_name="Product video",
            ),
        ),
    ]