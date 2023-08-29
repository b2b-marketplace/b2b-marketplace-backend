import csv

from _decimal import Decimal
from django.core.management.base import BaseCommand

from apps.products.models import Product


def get_sku_list(user):
    """Возвращает список уникальных артикулов товаров."""
    all_products = Product.objects.filter(user__username=user, is_deleted=False)
    all_skus = all_products.values_list("sku", flat=True)
    if not all_skus:
        raise ValueError(f"Пользователь {user} не имеет ни одного продукта.")
    return set(all_skus), all_products


def update_price_from_csv(file_path, username):
    """Обновляет цену товаров."""
    sku_set, all_products = get_sku_list(username)
    products_to_update = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["sku"] in sku_set:
                products_to_update.append(
                    Product(id=all_products.get(sku=row["sku"]).id, price=Decimal(row["price"]))
                )
    if not products_to_update:
        raise ValueError("Нет товаров для обновления.")

    Product.objects.bulk_update(products_to_update, fields=["price"])


class Command(BaseCommand):
    """
    Команда для обновления цен товаров из CSV-файла.

    Эта команда позволяет администратору обновлять цены товаров, связанных
    с определенным пользователем, используя данные из CSV-файла. CSV-файл
    должен содержать строки с колонками 'sku' и 'price', где 'sku' представляет
    уникальный код товара (артикул), а 'price' представляет новую цену,
    которая будет присвоена товару.

    Использование:
    python manage.py update_prices --username <username> --file_path <file_path>

    Аргументы:
        --username: Имя пользователя, чьи цены на товары нужно обновить.
        --file_path: Путь к CSV-файлу с обновленными ценами.

    Пример:
    python manage.py update_prices --username user1 --file_path /путь/к/файлу/с/ценами.csv
    """

    help = "Update price from csv file"

    def handle(self, *args, **options):
        username = options.get("username")
        file_path = options.get("file_path")

        try:
            update_price_from_csv(file_path=file_path, username=username)
            self.stdout.write(self.style.SUCCESS("Price updated"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found"))
        except ValueError as exp:
            self.stdout.write(self.style.ERROR(str(exp)))

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            required=True,
            help="The username of the user whose price to update.",
        )
        parser.add_argument(
            "--file_path",
            required=True,
            help="The path to the file to update.",
        )
