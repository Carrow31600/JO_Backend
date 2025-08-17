
import uuid
from django.db import models
from users.models import CustomUser
from events.models import Event
from offers.models import Offer

class OrderLine(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_places = models.PositiveIntegerField()
    order_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Ligne {self.id} - {self.event} - {self.offer} x {self.quantity}"
