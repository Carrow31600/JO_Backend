from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Offer
from .serializers import OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny] 
        else:
            permission_classes = [IsAdminUser]  
        return [permission() for permission in permission_classes]
