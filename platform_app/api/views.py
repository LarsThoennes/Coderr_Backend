from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Avg

from reviews_app.models import Review
from offers_app.models import Offer
from auth_app.models import User


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "review_count": Review.objects.count(),
            "average_rating": round(Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0,1),
            "offer_count": Offer.objects.count(),
            "business_profile_count": User.objects.filter(type='business').count(),
        })
