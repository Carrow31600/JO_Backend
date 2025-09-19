from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Offer
from .serializers import OfferSerializer
from decimal import Decimal

User = get_user_model()


# ***********************************************************
# Tests du modele
# ***********************************************************
class OfferModelTest(TestCase):

    def test_offer_creation_and_str(self):
        offer = Offer.objects.create(
            nom="VIP",
            nombre_places=10,
            prix=Decimal("150.00")
        )
        self.assertEqual(offer.nom, "VIP")
        self.assertEqual(offer.nombre_places, 10)
        self.assertEqual(offer.prix, Decimal("150.00"))
        self.assertEqual(str(offer), "VIP - 150.00 € (10 places)")


# ***********************************************************
# Tests du serializer
# ***********************************************************
class OfferSerializerTest(TestCase):

    def setUp(self):
        self.offer = Offer.objects.create(
            nom="Standard",
            nombre_places=5,
            prix=Decimal("50.00")
        )

    def test_serialization(self):
        serializer = OfferSerializer(self.offer)
        data = serializer.data
        self.assertEqual(data["nom"], "Standard")
        self.assertEqual(data["nombre_places"], 5)
        self.assertEqual(data["prix"], "50.00")  #Decimals en string

    def test_deserialization(self):
        data = {
            "nom": "Eco",
            "nombre_places": 3,
            "prix": "30.00"
        }
        serializer = OfferSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        offer = serializer.save()
        self.assertEqual(offer.nom, "Eco")
        self.assertEqual(offer.nombre_places, 3)
        self.assertEqual(offer.prix, Decimal("30.00"))


# ***********************************************************
# Tests API
# ***********************************************************
class OfferAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Utilisateur normal
        self.user = User.objects.create_user(
            username="client1",
            email="client@test.com",
            password="pass1234"
        )

        # Utilisateur admin
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="adminpass"
        )

        # Offre existante
        self.offer = Offer.objects.create(
            nom="Basic",
            nombre_places=2,
            prix=Decimal("20.00")
        )

    def test_list_offers_public(self):
        url = "/api/offers/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_offer_public(self):
        url = f"/api/offers/{self.offer.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom"], "Basic")

    def test_create_offer_requires_admin(self):
        url = "/api/offers/"
        data = {"nom": "Gold", "nombre_places": 5, "prix": "100.00"}

        # utilisateur normal interdit
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin autorisé
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)

    def test_update_offer_requires_admin(self):
        url = f"/api/offers/{self.offer.id}/"
        data = {"nom": "Basic Updated", "nombre_places": 3, "prix": "25.00"}

        # utilisateur normal interdit
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin autorisé
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.nom, "Basic Updated")

    def test_delete_offer_requires_admin(self):
        url = f"/api/offers/{self.offer.id}/"

        # utilisateur normal interdit
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin autorisé
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)
