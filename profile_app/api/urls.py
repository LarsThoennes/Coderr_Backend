from django.urls import path
from .views import DetailProfileView

urlpatterns = [
    path('<int:pk>/', DetailProfileView.as_view(), name='profile-detail')
]

