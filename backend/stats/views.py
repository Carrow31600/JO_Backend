from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import OrderLine
from django.db.models import Sum

# Pour chaque offre, donne le nombre de billets vendus par epreuve
class TicketsStatsByOfferView(APIView):

    def get(self, request):
        data = []

        # Regroupement par offre et épreuve
        # calcule de la quantité
        # classement par offre et épreuve
        stats = (
            OrderLine.objects
            .values('offer__id', 'offer__name', 'event__id', 'event__name')
            .annotate(tickets_sold=Sum('quantity'))
            .order_by('offer__id', 'event__id')
        )

        # création d'un dictionnaire par offres avec détail par épreuves
        offers_dict = {}
        for stat in stats:
            offer_id = stat['offer__id']
            if offer_id not in offers_dict:
                offers_dict[offer_id] = {
                    'offer_id': offer_id,
                    'offer_name': stat['offer__name'],
                    'events': []
                }
            offers_dict[offer_id]['events'].append({
                'event_id': stat['event__id'],
                'event_name': stat['event__name'],
                'tickets_sold': stat['tickets_sold']
            })

        data = list(offers_dict.values())
        return Response(data)
