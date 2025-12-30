from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters, status
from .serializers import ReviewCreateSerializer, ReviewsListSerializer, ReviewDetailsWithPrimaryKeySerializer
from reviews_app.models import Review
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404

class ReviewView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewsListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at'] 

    def get_queryset(self):
        queryset = Review.objects.all().annotate()

        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id:
            queryset = queryset.filter(business_user=int(business_user_id))

        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id:
            queryset = queryset.filter(reviewer=int(reviewer_id))

        return queryset
    

    def post(self, request):
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
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.reviewer != request.user:
            return Response(
                {"detail": "You do not have permission to delete this offer."},
                status=status.HTTP_403_FORBIDDEN
            )
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
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
        
        