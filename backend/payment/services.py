
#**********************************************************************
# Simulation d'un service de gestion du paiement
# renvoi true si paiement Ok et false sinon
# calcul le prix pour chaque ligne de commande et le total à payer
# si le paiement est true, appelle create_orders_from_payment pour crééer les lignes de commandes
# ***********************************************************************

import random
from offers.models import Offer

def mock_payment_service(user_id, lines):

    for line in lines:
        offer = Offer.objects.get(id=line['offer']) # on récupère l'offre dans la base
        line['price_per_unit'] = float(offer.prix) # on récupère le prix de l'offre
        line['total_price'] = line['quantity'] * offer.prix # on calcul le prix total de la ligne

    total_price = sum(line['total_price'] for line in lines) # on calcul le prix total de toutes les lignes
    success = random.random() < 1  # 100% de succès (à faire varier pour les tests)

    
    return {"success": success, "total_price": total_price, "lines": lines}
