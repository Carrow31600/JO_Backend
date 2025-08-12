from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserDetailSerializer
from .permissions import IsOwnerOrAdmin


# Gestion de la création d'un user
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()     # s'applique à tous les utilisateurs de la base
    permission_classes = [AllowAny]     # accès à tout le monde
    serializer_class = UserRegisterSerializer       # utilisation du sérializer qui gère l'enregistrement des users

# Gestion de l'affiche, de la modification et de la suppression d'un user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()      # s'applique à tous les utilisateurs de la base
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # accès uniquement à l'utilisateur authentifié et à l'admin
    serializer_class = UserDetailSerializer     # utilisation du serializer de modification de compte

    # récupère uniquement le compte de l'utilisateur connecté
    def get_object(self):
        return self.request.user

