import django_filters
from ..models import Offer


class OfferFilter(django_filters.FilterSet):
    """FilterSet for Offer list queries supporting price and delivery time filtering.

    Relies on annotated fields (annotated_min_price, annotated_min_delivery)
    that must be present on the queryset before filtering is applied.
    """

    creator_id = django_filters.NumberFilter(field_name='user')
    # Filter offers whose cheapest detail price is at least min_price
    min_price = django_filters.NumberFilter(
        field_name='annotated_min_price', lookup_expr='gte')
    # Filter offers whose fastest delivery is at most max_delivery_time days
    max_delivery_time = django_filters.NumberFilter(
        field_name='annotated_min_delivery', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']