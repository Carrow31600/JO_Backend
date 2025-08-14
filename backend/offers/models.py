from django.db import models

class Offer(models.Model):
    nom = models.CharField(max_length=100)
    nombre_places = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nom} - {self.prix} € ({self.nombre_places} places)"
