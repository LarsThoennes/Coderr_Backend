from rest_framework import serializers
from offers_app.models import Offer, OfferDetail, OfferFeature
from profile_app.models import Profile


class OfferDetailSerializer(serializers.ModelSerializer):
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


class OffersSerializer(serializers.ModelSerializer):
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
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username']

class FilterListDetailSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()
    class Meta:
        model = OfferDetail
        fields = [
            'price'
        ]

class OffersListSerializer(serializers.ModelSerializer):
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
    id = serializers.IntegerField(required=False)
    features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

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
