from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Avg

from reviews_app.models import Review
from offers_app.models import Offer
from auth_app.models import User


class BaseInfoView(APIView):
    """
    Provides aggregated statistics about the platform for public access.
    
    This endpoint is publicly accessible and does not require authentication.

    Returns:
        JSON response containing:
        - review_count: Total number of reviews on the platform.
        - average_rating: Average rating across all reviews, rounded to one decimal place.
        - offer_count: Total number of offers created by business users.
        - business_profile_count: Total number of business users on the platform.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Handle GET requests to retrieve the platform's base information.
        """
        return Response({
            "review_count": Review.objects.count(),
            "average_rating": round(Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0,1),
            "offer_count": Offer.objects.count(),
            "business_profile_count": User.objects.filter(type='business').count(),
        })
