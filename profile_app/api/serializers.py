from rest_framework import serializers
from django.db import transaction
from profile_app.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for full profile details.
    Includes related user information (username, email, type) as read-only fields.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at',
        ]

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer used for updating profile information.
    Supports updating related user's email and profile-specific fields.
    Email update is performed atomically.
    """
    email = serializers.EmailField(required=False)

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'location',
            'tel',
            'description',
            'working_hours',
            'email'
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Override the update method to allow updating the related user's email.
        Ensures atomic transaction for profile and user updates.

        Args:
            instance (Profile): Profile instance being updated.
            validated_data (dict): Validated update data.

        Returns:
            Profile: Updated profile instance.
        """
        email = validated_data.pop('email', None)

        if email is not None:
            instance.user.email = email
            instance.user.save(update_fields=['email'])

        return super().update(instance, validated_data)
    
class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing customer profiles.
    Includes read-only username and type fields from the related user.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'type'
        ]

class BusinessProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business profiles.
    Includes read-only username and type fields from the related user.
    Provides full business profile details such as contact info and working hours.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type'
        ]