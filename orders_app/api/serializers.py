from rest_framework import serializers
from orders_app.models import Order, OrderFeature
from offers_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
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
        return list(
            obj.order_features.values_list('name', flat=True)
        )

    def create(self, validated_data):
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
    class Meta:
        model = Order
        fields = [
            'status',
        ]