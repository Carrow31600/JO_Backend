from django.urls import path
from .views import MyOrdersListView, SalesStatsView

urlpatterns = [
    path("me/", MyOrdersListView.as_view(), name="my-orders"),
    path("stats/", SalesStatsView.as_view(), name="sales-stats"),
]
