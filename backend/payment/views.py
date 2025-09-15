# payment/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import mock_payment_service
from users.models import CustomUser
from orders.services import create_orders_from_payment


#*****************************************
# API de simulation du paiement
#*****************************************

class MockPaymentView(APIView):
    # Récupère les infos de la requete
    def post(self, request):
        user_id = request.data.get("user_id")
        lines = request.data.get("lines", [])

        # Vérifie que l'utilisateur existe
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur inconnu"}, status=status.HTTP_404_NOT_FOUND)

        # Appel du service mock_payment_service
        payment_result = mock_payment_service(user_id, lines)
        
        # Vérifie que le paiement s'est bien passé
        if not payment_result['success']:
            return Response({"detail": "Paiement échoué"}, status=status.HTTP_400_BAD_REQUEST)

        # Appel create_orders_from_payment pour créer les lignes de commandes
        order_lines = create_orders_from_payment(user, payment_result['lines'])
        return Response(order_lines, status=status.HTTP_201_CREATED)
