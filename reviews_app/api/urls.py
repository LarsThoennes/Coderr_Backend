from django.urls import path
from reviews_app.api.views import ReviewView, ReviewDetailView

urlpatterns = [
    path('reviews/', ReviewView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]