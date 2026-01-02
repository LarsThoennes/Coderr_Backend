from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from profile_app.models import Profile
from auth_app.models import User
from .serializers import ProfileSerializer, ProfileUpdateSerializer, CustomerProfileListSerializer, BusinessProfileListSerializer


class DetailProfileView(APIView):
    """
    Handles retrieving and updating detailed information of a single user profile.

    Permissions:
        - The user must be authenticated.
        - PATCH requests can only be performed by the owner of the profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve a single profile by its primary key (pk).

        Args:
            pk (int): ID of the profile to retrieve.

        Returns:
            Response: Serialized profile data including username, email, type, and profile fields.
        """
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Partially update a profile (PATCH).

        Only the profile owner can perform this action.

        Args:
            pk (int): ID of the profile to update.

        Returns:
            Response: Updated profile data.
            403 Forbidden if the user is not the owner.
        """
        profile = get_object_or_404(Profile, pk=pk)
        
        if profile.user != request.user:
            return Response(
                {"detail": "You do not have permission to edit this profile."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProfileUpdateSerializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = ProfileSerializer(profile)
        return Response(response_serializer.data)

class ListProfileView(APIView):
    """
    Retrieves a list of profiles filtered by type (business or customer).

    Permissions:
        - The user must be authenticated.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, type):
        """
        Retrieve all profiles of a given type.

        Args:
            type (str): The profile type to filter by ('business' or 'customer').

        Returns:
            Response: List of serialized profiles.
            400 Bad Request if an invalid type is provided.
        """
        if type not in ['business', 'customer']:
            return Response(
                {"detail": "Invalid profile type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profiles = Profile.objects.select_related('user').filter(
            user__type=type
        )
        if type == 'business':
            serializer = BusinessProfileListSerializer(profiles, many=True)
        else:
            serializer = CustomerProfileListSerializer(profiles, many=True)
        return Response(serializer.data)