''' simulation d'un paiement avec un prestataire externe qui renvoi TRUE si le paiement est passé
et FALSE dans le cas contraire.
Le mock calcul le prix de chaque ligne de commande et le prix total à payer
Si le paiement est TRUE, il appelle le service dans Orders pour créer les lignes de commandes'''

import random
from offers.models import Offer

def mock_payment_service(user_id, lines):

    for line in lines:
        offer = Offer.objects.get(id=line['offer'])
        line['price_per_unit'] = float(offer.prix)
        line['total_price'] = line['quantity'] * offer.prix

    total_price = sum(line['total_price'] for line in lines)
    success = random.random() < 0.8  # 80% de succès
    return {"success": success, "total_price": total_price, "lines": lines}
