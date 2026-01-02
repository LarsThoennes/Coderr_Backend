from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters, status
from .serializers import ReviewCreateSerializer, ReviewsListSerializer, ReviewDetailsWithPrimaryKeySerializer
from reviews_app.models import Review
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404

class ReviewView(ListCreateAPIView):
    """
    View for listing all reviews and creating a new review.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewsListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at'] 

    def get_queryset(self):
        """
        Returns a queryset of Review objects, optionally filtered by:
            - business_user_id: filters reviews for a specific business user
            - reviewer_id: filters reviews made by a specific customer
        """
        queryset = Review.objects.all().annotate()

        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id:
            queryset = queryset.filter(business_user=int(business_user_id))

        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id:
            queryset = queryset.filter(reviewer=int(reviewer_id))

        return queryset
    

    def post(self, request):
        """
        Creates a new Review.

        Only authenticated users with type 'customer' can create reviews.
        Validates the incoming data using ReviewCreateSerializer.
        """
        if request.user.type != 'customer':
            return Response(
                {"detail": "Only customer users can create reviews."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
    
class ReviewDetailView(APIView):
    """
    View for retrieving, updating, or deleting a single review by primary key.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
        Deletes a review identified by 'pk'.

        Only the original reviewer can delete their review.
        Returns 204 No Content on successful deletion.
        """
        review = get_object_or_404(Review, pk=pk)
        if review.reviewer != request.user:
            return Response(
                {"detail": "You do not have permission to delete this offer."},
                status=status.HTTP_403_FORBIDDEN
            )
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        """
        Partially updates a review identified by 'pk'.

        Only the original reviewer can update their review.
        Accepts partial fields validated by ReviewDetailsWithPrimaryKeySerializer.
        """
        review = get_object_or_404(Review, pk=pk)
        if review.reviewer != request.user:
            return Response(
                {"detail": "You do not have permission to edit this review."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ReviewDetailsWithPrimaryKeySerializer(
            review,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
        
        