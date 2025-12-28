from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OffersSerializer, OffersListSerializer, OfferPrimaryKeySerializer, AllDetailsForOfferSerializer, OfferDetailsWithPrimaryKeySerializer
from offers_app.models import Offer, OfferDetail
from offers_app.api.pagination import LargeResultsSetPagination
from rest_framework.generics import ListCreateAPIView
from django.db.models import Min
from rest_framework import filters, status
from django.shortcuts import get_object_or_404


class OffersView(ListCreateAPIView):
    serializer_class = OffersListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at'] 
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Offer.objects.all().annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )

        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(owner_id=int(creator_id))

        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(min_price__gte=float(min_price))

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=int(max_delivery_time))

        return queryset

    def post(self, request):
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
    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)

        serializer = OfferPrimaryKeySerializer(offer)

        return Response(serializer.data)
    
    def patch(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        print('offer', offer)

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
        offer = get_object_or_404(Offer, pk=pk)
        
        if offer.owner != request.user:
            return Response(
                {"detail": "You do not have permission to delete this offer."},
                status=status.HTTP_403_FORBIDDEN
            )
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllDetailsForOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = AllDetailsForOfferSerializer(offer_detail)
        return Response(serializer.data)