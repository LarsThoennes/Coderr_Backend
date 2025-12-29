from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderDetailsWithPrimaryKeySerializer
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from orders_app.models import Order
from auth_app.models import User

class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.type not in ['customer', 'business']:
            return Response({"detail": "Only customer or business users are allowed."},status=403)

        orders = get_list_or_404(Order, customer_user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        print('Creating order with data:', request.data)
        if request.user.type != 'customer':
            return Response(
                {"detail": "Only customer users can create orders."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
    
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "Only staff or admin users can delete orders."},
                status=status.HTTP_403_FORBIDDEN
            )
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        request_data = request.data.copy()
        order = get_object_or_404(Order, pk=pk)

        if order.business_user != request.user:
            return Response(
                {"detail": "You do not have permission to edit this order."},
                status=status.HTTP_403_FORBIDDEN)

        if request_data.get('status') not in ['in_progress', 'completed', 'cancelled']:
            return Response({"detail": "The request.data is not valid."}, status=403)

        serializer = OrderDetailsWithPrimaryKeySerializer(
            order,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class OrderInProgressCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
       business_user = get_object_or_404(User, pk=pk, type='business')
       orders = Order.objects.filter(business_user=business_user, status='in_progress')

       return Response({'order_count': len(orders)})

class OrderCompletedCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
       orders = Order.objects.filter(business_user=pk, status='completed')

       return Response({'completed_order_count': len(orders)})