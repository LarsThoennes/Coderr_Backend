from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile
from .serializers import ProfileSerializer

class DetailProfileView(RetrieveAPIView):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
