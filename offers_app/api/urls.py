from django.urls import path
from offers_app.api.views import ( OffersView, OfferDetailView, AllDetailsForOfferView )

urlpatterns = [
    path('offers/', OffersView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', AllDetailsForOfferView.as_view(), name='allofferdetail-detail'),
]
