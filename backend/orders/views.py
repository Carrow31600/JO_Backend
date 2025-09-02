from rest_framework import generics, permissions
from .models import OrderLine
from .serializers import OrderLineSerializer


class MyOrdersListView(generics.ListAPIView):
    """
    Retourne la liste des tickets de l'utilisateur connecté.
    """
    serializer_class = OrderLineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # On filtre uniquement les commandes de l'utilisateur connecté
        return OrderLine.objects.filter(user=self.request.user).select_related("event", "offer")
