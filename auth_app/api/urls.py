from django.urls import path
from .views import RegistrationView, CustomLoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', CustomLoginView.as_view()),
]
