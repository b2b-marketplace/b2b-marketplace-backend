import django_filters

from apps.orders.models import Order


class OrderFilter(django_filters.FilterSet):
    """Фильтр заказов.

    - id: номер заказа
    - status: статус заказа
    - created_at: дата создания заказа
    - sku: артикул товара
    - name: название товара
    - address: адрес доставки
    """

    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact", help_text="Номер заказа")
    status = django_filters.ChoiceFilter(choices=Order.Status.choices, help_text="Статус заказа")
    created_at = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date", help_text="Дата создания заказа"
    )
    sku = django_filters.CharFilter(
        field_name="order_products__sku",
        lookup_expr="icontains",
        distinct=True,
        help_text="Артикул товара(частичное совпадение)",
    )
    name = django_filters.CharFilter(
        field_name="order_products__name",
        lookup_expr="icontains",
        distinct=True,
        help_text="Название товара(частичное совпадение)",
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "created_at",
            "sku",
            "name",
        )


class BuyerOrderFilter(OrderFilter):
    """Фильтр заказов покупателя."""


class SupplierOrderFilter(OrderFilter):
    """Фильтр заказов продавца."""
