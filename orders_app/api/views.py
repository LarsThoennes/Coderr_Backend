from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderDetailsWithPrimaryKeySerializer
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from orders_app.models import Order
from auth_app.models import User

class OrdersView(APIView):
    """
    Handles listing and creation of orders.

    - GET:
      Returns all orders that belong to the authenticated customer or business user.
      Only users of type 'customer' or 'business' are allowed to access this endpoint.

    - POST:
      Allows only customer users to create a new order.
      The order is automatically associated with the authenticated customer.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all orders for the authenticated user.

        Returns:
            200 OK: A list of orders belonging to the authenticated customer.
            403 Forbidden: If the user type is not customer or business.
            404 Not Found: If no orders exist for the user.
        """
        if request.user.type not in ['customer', 'business']:
            return Response({"detail": "Only customer or business users are allowed."},status=403)

        orders = get_list_or_404(Order, customer_user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new order.

        Only users with type 'customer' are allowed to create orders.

        Returns:
            201 Created: Order was successfully created.
            403 Forbidden: If the user is not a customer.
            400 Bad Request: If the provided data is invalid.
        """
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
    """
    Handles update and deletion of a single order.

    - DELETE:
      Allows only staff or admin users to delete an order.

    - PATCH:
      Allows the assigned business user to update the order status.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
        Delete an order.

        Only staff or superusers are allowed to delete orders.

        Returns:
            204 No Content: Order was successfully deleted.
            403 Forbidden: If the user lacks permission.
            404 Not Found: If the order does not exist.
        """
        order = get_object_or_404(Order, pk=pk)
        
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"detail": "Only staff or admin users can delete orders."},
                status=status.HTTP_403_FORBIDDEN
            )
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        """
        Partially update an order.

        Only the assigned business user may update the order status.
        Allowed status values are: in_progress, completed, cancelled.

        Returns:
            200 OK: Order was successfully updated.
            403 Forbidden: If the user is not the assigned business user
                           or the status value is invalid.
            404 Not Found: If the order does not exist.
        """
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
    """
    Returns the number of orders with status 'in_progress'
    for a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
       """
        Retrieve the count of in-progress orders for a business user.

        Returns:
            200 OK: Number of orders currently in progress.
            404 Not Found: If the business user does not exist.
        """
       business_user = get_object_or_404(User, pk=pk, type='business')
       orders = Order.objects.filter(business_user=business_user, status='in_progress')

       return Response({'order_count': len(orders)})

class OrderCompletedCountView(APIView):
    """
    Returns the number of completed orders
    for a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
       """
        Retrieve the count of completed orders for a business user.

        Returns:
            200 OK: Number of completed orders.
            404 Not Found: If the business user does not exist.
        """
       orders = Order.objects.filter(business_user=pk, status='completed')

       return Response({'completed_order_count': len(orders)})