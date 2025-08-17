from .models import OrderLine
from tickets.services import create_ticket_for_order_line
from .serializers import OrderLineSerializer
from events.models import Event
from offers.models import Offer

# Création des lignes de commandes lorsque le paiement s'est bien passé
def create_orders_from_payment(user, lines):

    order_lines = []
    for line in lines:
        offer = Offer.objects.get(id=line['offer'])
        event = Event.objects.get(id=line['event'])

        order_line = OrderLine.objects.create(
            user=user,
            event=event,
            offer=offer,
            quantity=line['quantity'],
            total_price=line['total_price'],
            total_places=line['quantity'] * offer.nombre_places
        )

        # Appel du service de création du ticket dans une table non exposée
        create_ticket_for_order_line(order_line)
        order_lines.append(order_line)

    serializer = OrderLineSerializer(order_lines, many=True)
    return serializer.data
