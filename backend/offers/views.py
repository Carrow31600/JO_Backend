from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Offer
from .serializers import OfferSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

# personnalisation des autorisations
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]  # Liste et détail des offres accessible à tout le monde
        else:
            permission_classes = [IsAdminUser]  # User doit être admin pour créer, modifier, supprimer (tout le reste)
        return [permission() for permission in permission_classes]
