from django_filters import FilterSet, NumberFilter, CharFilter
from rest_framework.filters import SearchFilter

from apps.models import Car


class CarFilter(FilterSet):
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')
    capacity = CharFilter(field_name='capacity', lookup_expr='exact')
    category = NumberFilter(field_name='category_id')

    class Meta:
        model = Car
        fields = ('price_min', 'price_max', 'capacity', 'category')


class CarSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('name_only'):
            return ['name']
        return super().get_search_fields(view, request)
