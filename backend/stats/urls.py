from django.urls import path
from .views import TicketsStatsByOfferView

urlpatterns = [
    path('tickets-stats-by-offer/', TicketsStatsByOfferView.as_view(), name='tickets-stats-by-offer'),
]
