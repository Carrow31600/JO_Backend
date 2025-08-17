from django.db import models
from django.conf import settings
import uuid

# Les lignes de commandes sont envoyées depuis le frontend une fois le paiement réalisé
# on enregistre les lignes de commandes et on génère une clé unique pour chaque ligne
# cette clé unique sera utilisée pour créer le QRCode qui sera affiché coté frontend

class OrderLine(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    offer = models.ForeignKey("offers.Offer", on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Génération de la cle unique de la ligne de commande
    order_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Stock le nombre total de places dans le ticket (recalculé)
    total_places = models.PositiveIntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # total_places = nombre de place dans l'offre * quantité d'offre acheté
        if self.offer_id and self.quantity:
            self.total_places = self.offer.nombre_places * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderLine #{self.id} (user={self.user_id}, event={self.event_id}, offer={self.offer_id})"
