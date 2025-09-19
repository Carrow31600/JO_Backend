from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from sports.models import Sport
from lieux.models import Lieu
from events.models import Event
from offers.models import Offer
from orders.models import OrderLine
from .models import Ticket
from .services import create_ticket_for_order_line

User = get_user_model()


# ***********************************************************
# Tests du modele
# ***********************************************************
class TicketModelTest(TestCase):

    def setUp(self):
        # Création d’un utilisateur
        self.user = User.objects.create_user(
            username="ticketuser",
            email="ticket@test.com",
            password="pass1234"
        )
        # Données liées
        self.sport = Sport.objects.create(nom="Natation")
        self.lieu = Lieu.objects.create(nom="Piscine Olympique", code_postal="69000", ville="Lyon")
        self.event = Event.objects.create(sport=self.sport, lieu=self.lieu, date="2025-05-01")
        self.offer = Offer.objects.create(nom="Piscine Pass", prix=20, nombre_places=1)

        # Ligne de commande
        self.order_line = OrderLine.objects.create(
            user=self.user,
            event=self.event,
            offer=self.offer,
            quantity=1,
            total_price=Decimal("20.00"),
            total_places=1
        )

        # Ticket
        self.ticket = Ticket.objects.create(
            order=self.order_line,
            ticket_key="dummy-key"
        )

    def test_ticket_creation(self):
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(self.ticket.order, self.order_line)
        self.assertFalse(self.ticket.used)

    def test_str_representation(self):
        text = str(self.ticket)
        self.assertIn("Ticket", text)
        self.assertIn(str(self.order_line.id), text)


# ***********************************************************
# Tests du service
# ***********************************************************
class TicketServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="serviceuser",
            email="service@test.com",
            password="pass1234"
        )
        self.sport = Sport.objects.create(nom="Boxe")
        self.lieu = Lieu.objects.create(nom="Zénith", code_postal="31000", ville="Toulouse")
        self.event = Event.objects.create(sport=self.sport, lieu=self.lieu, date="2025-06-01")
        self.offer = Offer.objects.create(nom="RingSide", prix=50, nombre_places=2)

        self.order_line = OrderLine.objects.create(
            user=self.user,
            event=self.event,
            offer=self.offer,
            quantity=1,
            total_price=Decimal("50.00"),
            total_places=2
        )

    def test_create_ticket_for_order_line(self):
        ticket = create_ticket_for_order_line(self.order_line)

        # test qu’un ticket a été créé
        self.assertIsInstance(ticket, Ticket)
        self.assertEqual(ticket.order, self.order_line)

        # La clé doit contenir secret_key et order_key
        self.assertIn(str(self.user.secret_key), ticket.ticket_key)
        self.assertIn(str(self.order_line.order_key), ticket.ticket_key)

        # Un seul ticket par OrderLine (OneToOne)
        with self.assertRaises(Exception):
            Ticket.objects.create(
                order=self.order_line,
                ticket_key="another-key"
            )
