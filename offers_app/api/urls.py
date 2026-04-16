from django.urls import path
from .views import OfferListCreateView, OfferDetailRetrieveView, OfferRetrieveUpdateDestroyView

urlpatterns = [
    path('', OfferListCreateView.as_view(), name='offer-list-create'),
    path('<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-detail'),
    path('details/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offerdetail-detail'),
]