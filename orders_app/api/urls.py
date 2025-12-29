from django.urls import path
from orders_app.api.views import OrdersView, OrderDetailView, OrderInProgressCountView, OrderCompletedCountView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:pk>/', OrderInProgressCountView.as_view(), name='order-count-in-progress-detail'),
    path('completed-order-count/<int:pk>/', OrderCompletedCountView.as_view(), name='order-count-complete-detail'),
]