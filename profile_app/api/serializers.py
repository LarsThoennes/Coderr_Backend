from rest_framework import serializers
from django.db import transaction
from profile_app.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
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
        email = validated_data.pop('email', None)

        if email is not None:
            instance.user.email = email
            instance.user.save(update_fields=['email'])

        return super().update(instance, validated_data)
    
class ProfileListSerializer(serializers.ModelSerializer):
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