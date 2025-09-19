from django.test import TestCase
from django.contrib.auth import get_user_model
from events.models import Event
from sports.models import Sport
from lieux.models import Lieu
from offers.models import Offer
from .models import OrderLine
from .serializers import OrderLineSerializer
from .services import create_orders_from_payment
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
import datetime

User = get_user_model()


# ***********************************************************
# Tests du modele
# ***********************************************************
class OrderLineModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="pass1234"
        )
        self.sport = Sport.objects.create(nom="Football")
        self.lieu = Lieu.objects.create(nom="Stade de France", code_postal="93200", ville="Saint-Denis")
        self.event = Event.objects.create(sport=self.sport, lieu=self.lieu, date="2025-01-01")
        self.offer = Offer.objects.create(nom="VIP", prix=100, nombre_places=2)

    def test_orderline_creation(self):
        order = OrderLine.objects.create(
            user=self.user,
            event=self.event,
            offer=self.offer,
            quantity=2,
            total_price=Decimal("200.00"),
            total_places=4
        )
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, Decimal("200.00"))
        self.assertEqual(order.total_places, 4)

    def test_str_representation(self):
        order = OrderLine.objects.create(
            user=self.user,
            event=self.event,
            offer=self.offer,
            quantity=1,
            total_price=Decimal("100.00"),
            total_places=2
        )
        self.assertIn("Ligne", str(order))
        self.assertIn("VIP", str(order))


# ***********************************************************
# Tests du serializer
# ***********************************************************
class OrderLineSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser2",
            email="test2@test.com",
            password="pass1234"
        )
        self.sport = Sport.objects.create(nom="Basketball")
        self.lieu = Lieu.objects.create(nom="Accor Arena", code_postal="75012", ville="Paris")
        self.event = Event.objects.create(sport=self.sport, lieu=self.lieu, date="2025-02-01")
        self.offer = Offer.objects.create(nom="Standard", prix=50, nombre_places=1)
        self.order = OrderLine.objects.create(
            user=self.user,
            event=self.event,
            offer=self.offer,
            quantity=3,
            total_price=Decimal("150.00"),
            total_places=3
        )

    def test_serialization(self):
        serializer = OrderLineSerializer(self.order)
        data = serializer.data
        self.assertEqual(data["quantity"], 3)
        self.assertEqual(data["offer_name"], "Standard")
        self.assertIn("event_name", data)

    def test_deserialization(self):
        data = {
            "user": self.user.id,
            "event": self.event.id,
            "offer": self.offer.id,
            "quantity": 2,
            "total_price": "100.00",
            "total_places": 2,
        }
        serializer = OrderLineSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


# ***********************************************************
# Tests du service
# ***********************************************************
class CreateOrdersFromPaymentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="payuser",
            email="pay@test.com",
            password="pass1234"
        )
        self.sport = Sport.objects.create(nom="Tennis")
        self.lieu = Lieu.objects.create(nom="Roland Garros", code_postal="75016", ville="Paris")
        self.event = Event.objects.create(sport=self.sport, lieu=self.lieu, date="2025-03-01")
        self.offer = Offer.objects.create(nom="Premium", prix=75, nombre_places=1)

    def test_create_orders_from_payment(self):
        lines = [
            {"event": self.event.id, "offer": self.offer.id, "quantity": 2, "total_price": Decimal("150.00")}
        ]
        orders = create_orders_from_payment(self.user, lines)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["quantity"], 2)
        self.assertEqual(orders[0]["total_price"], "150.00")


# ***********************************************************
# Tests API
# ***********************************************************
class OrdersAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Création utilisateur client
        self.user = User.objects.create_user(
            username="client1",
            email="client@test.com",
            password="pass1234"
        )

        # Création utilisateur admin
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="adminpass"
        )

        # Données liées
        self.sport = Sport.objects.create(nom="Handball")
        self.lieu = Lieu.objects.create(nom="Arena", code_postal="31000", ville="Toulouse")
        self.event = Event.objects.create(sport=self.sport, lieu=self.lieu, date="2025-04-01")
        self.offer = Offer.objects.create(nom="Eco", prix=30, nombre_places=1)

        # Commande associée au client
        self.order = OrderLine.objects.create(
            user=self.user,
            event=self.event,
            offer=self.offer,
            quantity=1,
            total_price=Decimal("30.00"),
            total_places=1
        )

    def test_my_orders_requires_auth(self):
        url = "/api/orders/me/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_my_orders_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = "/api/orders/me/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.order.id)

    def test_sales_stats_requires_admin(self):
        self.client.force_authenticate(user=self.user)
        url = "/api/orders/stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_stats_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = "/api/orders/stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("offers", response.data)
        self.assertIn("global", response.data)
