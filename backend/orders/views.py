from rest_framework import generics, permissions
from .models import OrderLine
from .serializers import OrderLineSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum

# **********************************************************
# Liste des tickets de l'utilisateur connecté
# **********************************************************

class MyOrdersListView(generics.ListAPIView):

    serializer_class = OrderLineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # On filtre uniquement les commandes de l'utilisateur connecté
        return OrderLine.objects.filter(user=self.request.user).select_related("event", "offer")


# ***********************************************************
# Statistiques de ventes
#************************************************************

class SalesStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Regrouper par offre
        stats = (
            OrderLine.objects
            .values("offer__nom") # regroupement par nom d'offre
            .annotate(
                total_tickets=Sum("total_places"),# total du nombre de places vendues
                total_revenue=Sum("total_price") # CA total
            )
            .order_by("offer__nom") # tri par nom d'offre
        )

        # Totaux globaux
        global_totals = {
            "total_tickets": sum(s["total_tickets"] or 0 for s in stats),
            "total_revenue": sum(float(s["total_revenue"] or 0) for s in stats),
        }

        return Response({
            "offers": stats,
            "global": global_totals
        })