from django.urls import path
from offers_app.api.views import ( OffersView, OfferDetailView )

urlpatterns = [
    path('', OffersView.as_view(), name='offer-list-create'),
    path('<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
]
