from django.db import models
from sports.models import Sport
from lieux.models import Lieu

class Event(models.Model):
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, related_name='events')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()

    def __str__(self):
        return f"{self.sport.nom} @ {self.lieu.nom} le {self.date}"
