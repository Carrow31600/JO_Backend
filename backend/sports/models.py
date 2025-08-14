from django.db import models

class Sport(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='sports_photos/', blank=True, null=True)

    def __str__(self):
        return self.nom