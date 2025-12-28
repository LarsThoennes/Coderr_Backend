from django.urls import path
from offers_app.api.views import AllDetailsForOfferView

urlpatterns = [
    path('<int:pk>/', AllDetailsForOfferView.as_view(), name='allofferdetail-detail'),
]
