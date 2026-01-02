from rest_framework import serializers
from offers_app.models import Offer, OfferDetail, OfferFeature
from profile_app.models import Profile


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail model.
    - Features are represented as a list of strings.
    - Price is an integer.
    Used when creating or displaying individual offer details.
    """
    features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    price = serializers.IntegerField()

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',    
            'offer_type', 
        ]

    def to_representation(self, instance):
        """
        Convert features to a list of names for read operations.
        """
        data = super().to_representation(instance)
        data['features'] = list(
            instance.features.values_list('name', flat=True)
        )
        return data


class OffersSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and displaying Offer instances including nested OfferDetails.
    - Nested serializer for details (OfferDetailSerializer)
    - Supports bulk creation of features.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]

    def create(self, validated_data):
        """
        Create an Offer with nested OfferDetails and Features.
        """
        details_data = validated_data.pop('details')
        request = self.context['request']

        offer = Offer.objects.create(
            owner=request.user,
            **validated_data
        )

        for detail_data in details_data:
            features = detail_data.pop('features', [])

            detail = OfferDetail.objects.create(
                offer=offer,
                **detail_data
            )

            OfferFeature.objects.bulk_create([
                OfferFeature(detail=detail, name=feature)
                for feature in features
            ])

        return offer
    
class OfferListDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for minimal OfferDetail information.
    Returns only ID and URL.
    """
    url = serializers.SerializerMethodField()
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'url'
        ]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

class ProfileMiniSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for Profile information.
    Includes first_name, last_name, and username only.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username']

class FilterListDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for filtering operations.
    Currently returns only the price.
    """
    price = serializers.IntegerField()
    class Meta:
        model = OfferDetail
        fields = [
            'price'
        ]

class OffersListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Offers.
    - Includes minimal price and delivery time.
    - Includes minimal profile information of the owner.
    """
    details = OfferListDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.IntegerField(source='owner.id', read_only=True)
    user_details = ProfileMiniSerializer(
        source='owner.profile',
        read_only=True
    )

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)

        if not prices:
            return None

        return int(min(prices))
    
    def get_min_delivery_time(self, obj):
        delivery_times = obj.details.values_list('delivery_time_in_days', flat=True)

        if not delivery_times:
            return None

        return int(min(delivery_times))


    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

class OfferPrimaryKeySerializer(serializers.ModelSerializer):
    """
    Serializer for a single Offer with minimal information.
    - Includes min_price and min_delivery_time.
    """
    details = OfferListDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.IntegerField(source='owner.id', read_only=True)

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)

        if not prices:
            return None

        return int(min(prices))
    
    def get_min_delivery_time(self, obj):
        delivery_times = obj.details.values_list('delivery_time_in_days', flat=True)

        if not delivery_times:
            return None

        return int(min(delivery_times))
    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time'
        ]


class AllDetailsForOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for all details of a specific OfferDetail including features.
    """
    features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    price = serializers.IntegerField()

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',    
            'offer_type', 
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['features'] = list(
            instance.features.values_list('name', flat=True)
        )
        return data
    
class OfferDetailWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing/updating OfferDetails.
    - ID is optional for updating existing details
    - Features are passed as a list of strings.
    """
    id = serializers.IntegerField(required=False)
    features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    price = serializers.IntegerField()

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['features'] = list(
            instance.features.values_list('name', flat=True)
        )
        return data


class OfferDetailsWithPrimaryKeySerializer(serializers.ModelSerializer):
    """
    Serializer for updating an Offer with nested OfferDetails.
    - Supports both updating existing details and adding new ones.
    - Features are replaced if new ones are provided.
    """
    details = OfferDetailWriteSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details'
        ]

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            existing_details = {
                detail.offer_type: detail
                for detail in instance.details.all()
            }

            for detail_data in details_data:
                features = detail_data.pop('features', None)
                offer_type = detail_data.get('offer_type')

                if offer_type in existing_details:
                    detail = existing_details[offer_type]
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
                else:
                    detail = OfferDetail.objects.create(
                        offer=instance,
                        **detail_data
                    )

                if features is not None:
                    detail.features.all().delete()

                    OfferFeature.objects.bulk_create([
                        OfferFeature(detail=detail, name=name)
                        for name in features
                    ])

        return instance
