from django.urls import path
from .views import DetailProfileView, ListProfileView

urlpatterns = [
    path('profile/<int:pk>/', DetailProfileView.as_view(), name='profile-detail'),
    path('profiles/<str:type>/', ListProfileView.as_view(), name='profile-type-list'),
]

