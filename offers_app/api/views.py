from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import OffersSerializer, OffersListSerializer, OfferPrimaryKeySerializer, AllDetailsForOfferSerializer, OfferDetailsWithPrimaryKeySerializer
from offers_app.models import Offer, OfferDetail
from offers_app.api.pagination import LargeResultsSetPagination
from rest_framework.generics import ListCreateAPIView
from django.db.models import Min
from rest_framework import filters, status
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class OffersView(ListCreateAPIView):
    """
    Handles listing and creation of offers.

    - GET:
      Returns a paginated list of all offers.
      Supports:
        - ordering (updated_at, min_price)
        - searching (title, description)
        - filtering by creator, minimum price and maximum delivery time

    - POST:
      Allows business users to create new offers.
      Customer users are not permitted to create offers.
    """
    serializer_class = OffersListSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at'] 
    search_fields = ['title', 'description']

    def get_permissions(self):
        """
        - AllowAny for GET requests
        - IsAuthenticated for POST requests
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Returns a queryset of offers annotated with:
        - min_price: lowest price across all offer details
        - min_delivery_time: shortest delivery time across all offer details

        Optional query parameters:
        - creator_id: filter offers by owner
        - min_price: filter offers with minimum price >= value
        - max_delivery_time: filter offers with delivery time <= value
        """
        queryset = Offer.objects.all().annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )

        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            try:
                creator_id_int = int(creator_id)
            except ValueError:
                raise serializers.ValidationError({
                    "creator_id": "Must be an integer."
                })
            queryset = queryset.filter(owner_id=creator_id_int)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            try:
                min_price_float = float(min_price)
            except ValueError:
                raise serializers.ValidationError({
                    "min_price": "Must be a numeric value."
                })
            queryset = queryset.filter(min_price__gte=min_price_float)

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                max_delivery_time_int = int(max_delivery_time)
            except ValueError:
                raise serializers.ValidationError({
                    "max_delivery_time": "Must be an integer."
                })
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time_int)

        return queryset

    def post(self, request):
        """
        Creates a new offer.

        Only users with type 'business' are allowed to create offers.
        """
        if request.user.type != 'business':
            return Response(
                {"detail": "Only business users can create offers."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = OffersSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
    
class OfferDetailView(APIView):
    """
    Handles retrieve, update and deletion of a single offer.
    """
    def get(self, request, pk):
        """
        Returns basic information about a single offer identified by its ID.
        """
        offer = get_object_or_404(Offer, pk=pk)

        serializer = OfferPrimaryKeySerializer(offer)

        return Response(serializer.data)
    
    def patch(self, request, pk):
        """
        Partially updates an offer.

        Only the owner of the offer is allowed to update it.
        """
        offer = get_object_or_404(Offer, pk=pk)

        if offer.owner != request.user:
            return Response(
                {"detail": "You do not have permission to edit this offer."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OfferDetailsWithPrimaryKeySerializer(
            offer,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def delete(self, request, pk):
        """
        Deletes an offer.

        Only the owner of the offer is allowed to delete it.
        """
        offer = get_object_or_404(Offer, pk=pk)
        
        if offer.owner != request.user:
            return Response(
                {"detail": "You do not have permission to delete this offer."},
                status=status.HTTP_403_FORBIDDEN
            )
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllDetailsForOfferView(APIView):
    """
    Returns all details for a specific offer detail entry.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieves a single OfferDetail including all related information.
        """
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = AllDetailsForOfferSerializer(offer_detail)
        return Response(serializer.data)