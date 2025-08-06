from django_filters import FilterSet, NumberFilter, CharFilter

from apps.models import Car


class CarFilter(FilterSet):
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')
    capacity = CharFilter(field_name='capacity', lookup_expr='exact')
    category = NumberFilter(field_name='category_id')

    class Meta:
        model = Car
        fields = ('price_min', 'price_max', 'capacity', 'category')
