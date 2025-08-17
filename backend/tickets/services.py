
from .models import Ticket

# service de création du ticket à partir de clé user et de la clé orders
def create_ticket_for_order_line(order_line):

    user_secret = str(order_line.user.secret_key)
    order_key = str(order_line.order_key)
    ticket_key = f"{user_secret}-{order_key}"
    ticket = Ticket.objects.create(order=order_line, ticket_key=ticket_key)
    return ticket
