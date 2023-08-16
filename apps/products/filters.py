import django_filters
from django.db.models import IntegerField, Q, Value

from apps.products.models import Category, Product


class ProductFilter(django_filters.FilterSet):
    """Фильтр по товарам.

    Возможные параметры:
        - category: slug категории (точное совпадение)
        - name: название товара (частичное совпадение)
        - min_quantity: минимальный заказ
        - ordering: сортировка по цене
    """

    category = django_filters.CharFilter(
        field_name="category__slug", help_text="Категория товара (slug)"
    )
    name = django_filters.CharFilter(
        method="filter_by_name", help_text="Название товара (частичное совпадение)"
    )
    min_quantity = django_filters.NumberFilter(
        field_name="wholesale_quantity", lookup_expr="gt", help_text="Минимальный заказ"
    )
    ordering = django_filters.OrderingFilter(
        fields=("price",), field_labels={"price": "Цена"}, help_text="Сортировка по цене"
    )

    class Meta:
        model = Product
        #  ! поле name обязательно должно быть последним элементом в fields, т.к. возвращает union
        #  https://docs.djangoproject.com/en/4.2/ref/models/querysets/#union
        fields = ("category", "min_quantity", "ordering", "name")

    def filter_by_name(self, queryset, name, value):
        """Фильтрация по названию товара.

        Фильтрация производится:
            1) по вхождению в начало названия товара
            2) по вхождению в произвольном месте названия товара
        Результирующий список сортируется от группы 1 к группе 2.
        """
        name_starts = Q(name__istartswith=value)
        name_contains = Q(name__icontains=value)
        qs1 = queryset.filter(name_starts).annotate(order=Value(0, IntegerField()))
        qs2 = (
            queryset.filter(name_contains)
            .exclude(name_starts)
            .annotate(order=Value(1, IntegerField()))
        )
        return qs1.union(qs2).order_by("order")


class CategoryFilter(django_filters.FilterSet):
    """Фильтр по категориям.

    Возможные параметры:
        - name: название категории (частичное совпадение)
        - slug: название товара (точное совпадение)
    """

    name = django_filters.CharFilter(
        lookup_expr="icontains", help_text="Название категории (частичное совпадение)"
    )
    slug = django_filters.CharFilter(lookup_expr="iexact", help_text="Slug категории")

    class Meta:
        model = Category
        fields = ("name", "slug")
