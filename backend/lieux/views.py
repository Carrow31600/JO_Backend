from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lieu
from .serializers import LieuSerializer

class LieuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ville']  
    search_fields = ['nom', 'ville']  
    ordering_fields = ['nom', 'ville']
    ordering = ['nom']
