from django.urls import path
from .views import TicketScanView

urlpatterns = [
    path('ticket-scan/', TicketScanView.as_view(), name='ticket-scan'),
]
