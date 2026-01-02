import django_filters
from offers_app.models import Offer


class OfferFilter(django_filters.FilterSet):
    """
    FilterSet for the Offer model to allow filtering API results based on
    creator, minimum price, and maximum delivery time.

    Filters:
    - creator_id: Filters offers by the owner's user ID.
    - min_price: Filters offers that have a detail price greater than or equal to this value.
    - max_delivery_time: Filters offers that have a delivery time less than or equal to this value.
    """
    creator_id = django_filters.NumberFilter(field_name='owner__id')
    min_price = django_filters.NumberFilter(
        field_name='details__price', lookup_expr='gte'
    )
    max_delivery_time = django_filters.NumberFilter(
        field_name='details__delivery_time_in_days', lookup_expr='lte'
    )

    class Meta:
        model = Offer
        fields = [
            'creator_id',
            'min_price',
            'max_delivery_time',
        ]
