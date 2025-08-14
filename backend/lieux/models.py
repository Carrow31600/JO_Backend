from django.db import models

class Lieu(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='lieux_photos/', blank=True, null=True)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nom} - {self.ville}"
