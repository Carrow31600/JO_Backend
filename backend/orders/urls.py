from django.urls import path
from .views import MyOrdersListView

urlpatterns = [
    path("me/", MyOrdersListView.as_view(), name="my-orders"),
]
