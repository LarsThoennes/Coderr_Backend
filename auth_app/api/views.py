from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """
    Handles user registration.

    This endpoint allows new users to register on the platform.
    After successful registration, an authentication token is
    generated and returned to the client.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Creates a new user account.

        Request Body:
        - username
        - email
        - password
        - type (customer or business)

        Response:
        - authentication token
        - username
        - email
        - user ID
        """

        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED
        )

class CustomLoginView(APIView):
    """
    Handles user authentication (login).

    This endpoint authenticates a user using username and password.
    If credentials are valid, an authentication token is returned.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticates a user and returns an auth token.

        Request Body:
        - username
        - password

        Response:
        - authentication token
        - username
        - email
        - user ID

        Errors:
        - 400: Invalid credentials
        """
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=400
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        })