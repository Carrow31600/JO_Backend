
from django.db import models
from orders.models import OrderLine

# table non exposée qui stock la clé final du ticket (concaténation de la clé user et de la cle orders)
# le champ used sert à savoir si le ticket à déjà été utilisé
class Ticket(models.Model):
    order = models.OneToOneField(OrderLine, on_delete=models.CASCADE)
    ticket_key = models.CharField(max_length=200, unique=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket {self.id} pour order {self.order.id}"
