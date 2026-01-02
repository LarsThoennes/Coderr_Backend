from rest_framework import serializers
from django.contrib.auth import get_user_model
from profile_app.models import Profile

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles:
    - validation of unique email addresses
    - password confirmation
    - creation of a new user
    - automatic creation of an associated user profile
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeated_password', 'type')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Performs cross-field validation.

        Validations:
        - Ensures the email address is unique
        - Ensures password and repeated_password match
        """
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'Email is already in use.'
            })

        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })

        return data

    def create(self, validated_data):
        """
        Creates a new user and its related profile.

        Steps:
        - Remove repeated_password from validated data
        - Create the user using Django's create_user method
        - Automatically create an empty Profile instance for the user
        """
        validated_data.pop('repeated_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            type=validated_data['type'],
        )

        Profile.objects.create(user=user)

        return user