from rest_framework import serializers
from reviews_app.models import Review
from auth_app.models import User


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new review.

    Fields:
    - business_user: The business user receiving the review. Must be of type 'business'.
    - reviewer: The customer creating the review (read-only, automatically set to the authenticated user).
    - rating: Integer rating value.
    - description: Textual description of the review.
    - created_at, updated_at: Timestamps (read-only).
    """
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
        """
        Creates a new Review instance, automatically setting the reviewer
        to the currently authenticated user.
        """
        request = self.context['request']

        review = Review.objects.create(
            business_user=validated_data['business_user'],
            reviewer=request.user,
            rating=validated_data['rating'],
            description=validated_data['description'],
        )

        return review
    
class ReviewsListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing reviews.

    Fields:
    - business_user: The business user being reviewed.
    - reviewer: The ID of the reviewer (read-only).
    - rating: Integer rating value.
    - description: Review text.
    - created_at, updated_at: Timestamps (read-only).
    """
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
    """
    Serializer for updating an existing review by primary key.

    Only the 'rating' and 'description' fields can be modified by the reviewer.
    Other fields are read-only.
    """
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