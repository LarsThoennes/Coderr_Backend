from django.urls import path
from .views import DetailProfileView, ListProfileView

urlpatterns = [
    path('<int:pk>/', DetailProfileView.as_view(), name='profile-detail'),
    path('<str:type>/', ListProfileView.as_view(), name='profile-type-list'),
]

