from rest_framework import serializers
from reviews_app.models import Review
from auth_app.models import User


class ReviewCreateSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type='business')
    )
    reviewer = serializers.IntegerField(
        source='reviewer.id',
        read_only=True
    )
    rating = serializers.IntegerField()
    description = serializers.CharField()

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'reviewer',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        request = self.context['request']

        review = Review.objects.create(
            business_user=validated_data['business_user'],
            reviewer=request.user,
            rating=validated_data['rating'],
            description=validated_data['description'],
        )

        return review
    
class ReviewsListSerializer(serializers.ModelSerializer):
    reviewer = serializers.IntegerField(
        source='reviewer.id',
        read_only=True
    )
    rating = serializers.IntegerField()
    description = serializers.CharField()

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]

class ReviewDetailsWithPrimaryKeySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'business_user',
            'reviewer',
            'created_at',
            'updated_at',
        ]