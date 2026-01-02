from rest_framework import serializers
from orders_app.models import Order, OrderFeature
from offers_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing orders.

    This serializer:
    - Accepts an `offer_detail_id` to create an order from an OfferDetail
    - Automatically sets customer and business users
    - Copies relevant data from the related OfferDetail
    - Attaches all selected features to the order
    """
    offer_detail_id = serializers.IntegerField(write_only=True)
    price = serializers.IntegerField(read_only=True)
    customer_user = serializers.IntegerField(
        source='customer_user.id',
        read_only=True
    )
    business_user = serializers.IntegerField(
        source='business_user.id',
        read_only=True
    )
    features = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'id',
            'offer_detail_id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]

    def validate_offer_detail_id(self, value):
        """
        Validate that the provided OfferDetail exists.

        Also optimizes database access by prefetching related data.

        Raises:
            ValidationError: If the OfferDetail does not exist.
        """
        try:
            return OfferDetail.objects.select_related(
                'offer__owner'
            ).prefetch_related(
                'features'
            ).get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                "OfferDetail mit dieser ID existiert nicht."
            )
        
    def get_features(self, obj):
        """
        Return a list of feature names associated with the order.
        """
        return list(
            obj.order_features.values_list('name', flat=True)
        )

    def create(self, validated_data):
        """
        Create a new Order instance.

        - Assigns the authenticated user as customer
        - Assigns the offer owner as business user
        - Copies offer detail values into the order
        - Automatically sets order status to 'in_progress'
        - Copies all features from OfferDetail into OrderFeature
        """
        request = self.context['request']
        offer_detail = validated_data.pop('offer_detail_id')

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.owner,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            offer_type=offer_detail.offer_type,
            status='in_progress',
        )

        OrderFeature.objects.bulk_create([
            OrderFeature(
                features=order,
                name=feature.name
            )
            for feature in offer_detail.features.all()
        ])

        return order


class OrderDetailsWithPrimaryKeySerializer(serializers.ModelSerializer):
    """
    Serializer for partial updates of an order.

    Currently allows updating only the order status.
    """
    class Meta:
        model = Order
        fields = [
            'status',
        ]