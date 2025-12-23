from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from profile_app.models import Profile
from auth_app.models import User
from .serializers import ProfileSerializer, ProfileUpdateSerializer, ProfileListSerializer
from django_filters.rest_framework import DjangoFilterBackend


class DetailProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk):
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
    permission_classes = [IsAuthenticated]

    def get(self, request, type):
        if type not in ['business', 'customer']:
            return Response(
                {"detail": "Invalid profile type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profiles = Profile.objects.select_related('user').filter(
            user__type=type
        )

        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data)