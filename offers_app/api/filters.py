import django_filters
from ..models import Offer

class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='user')
    min_price = django_filters.NumberFilter(
        field_name='annotated_min_price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(
        field_name='annotated_min_delivery', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']