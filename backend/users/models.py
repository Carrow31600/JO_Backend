import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# Création d'un modèle user personnalisé 
# Ajout des champs firstname, email et secret_key au modèle user standard

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    secret_key = models.UUIDField(default=uuid.uuid4, editable=False)

    # choix du champ affiché dans l'interface admin de django pour le modèle user
    def __str__(self):
        return self.username
