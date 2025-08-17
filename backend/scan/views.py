
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tickets.models import Ticket
from users.models import CustomUser

# vérification de la validité du ticket scanné
class TicketScanView(APIView):

    # Récupère les éléments de la requete
    def post(self, request):
        user_id = request.data.get("user_id")
        order_key = request.data.get("order_key")

        # Vérifie que l'utilisataeur existe
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur inconnu"}, status=status.HTTP_404_NOT_FOUND)

        # reconstitutation la clé du billet
        ticket_key_to_check = f"{user.secret_key}-{order_key}"

        # Vérifie que le ticket existe bien dans la table tickets et qu'il n'est pas déjà utilisé
        try:
            ticket = Ticket.objects.get(ticket_key=ticket_key_to_check)
        except Ticket.DoesNotExist:
            return Response({"detail": "Billet invalide"}, status=status.HTTP_400_BAD_REQUEST)

        if ticket.used:
            return Response({"detail": "Billet déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        # si le ticket est valide, on passe used à true pour enregistrer que le ticket a été utilisé
        ticket.used = True
        ticket.save()
        return Response({"detail": "Billet valide"}, status=status.HTTP_200_OK)
