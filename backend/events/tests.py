from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from .models import Event
from sports.models import Sport
from lieux.models import Lieu
from .serializers import EventSerializer


# *****************************
# TESTS DU MODELE
# *****************************
class EventModelTest(TestCase):

    def setUp(self):
        # Création d'un Sport
        self.sport = Sport.objects.create(
            nom="Football",
            description="Sport collectif populaire"
        )
        # Création d'un Lieu
        self.lieu = Lieu.objects.create(
            nom="Stade de Paris",
            description="Grand stade national",
            code_postal="75000",
            ville="Paris"
        )
        self.date = timezone.now().date()

    def test_event_creation(self):
        # test la création d'un event
        event = Event.objects.create(
            sport=self.sport,
            lieu=self.lieu,
            date=self.date
        )
        self.assertEqual(event.sport.nom, "Football")
        self.assertEqual(event.lieu.nom, "Stade de Paris")
        self.assertEqual(event.lieu.ville, "Paris")
        self.assertEqual(event.date, self.date)

    def test_event_str_representation(self):
        #Vérifie que __str__ retourne la bonne chaine
        event = Event.objects.create(
            sport=self.sport,
            lieu=self.lieu,
            date=self.date
        )
        expected_str = f"Football @ Stade de Paris le {self.date}"
        self.assertEqual(str(event), expected_str)


# ******************************
# TESTS DU SERIALIZER
# ******************************
class EventSerializerTest(TestCase):

    def setUp(self):
        self.sport = Sport.objects.create(
            nom="Basketball",
            description="Sport collectif en salle"
        )
        self.lieu = Lieu.objects.create(
            nom="Gymnase",
            description="Salle couverte",
            code_postal="69000",
            ville="Lyon"
        )
        self.event = Event.objects.create(
            sport=self.sport,
            lieu=self.lieu,
            date=timezone.now().date()
        )

    def test_event_serialization(self):
        # test que les bons champs sont renvoyés
        serializer = EventSerializer(self.event)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"id", "lieu", "sport", "date"})
        self.assertEqual(data["sport"], self.sport.id)
        self.assertEqual(data["lieu"], self.lieu.id)

    def test_event_deserialization(self):
        # test la création d'un event valide
        data = {
            "sport": self.sport.id,
            "lieu": self.lieu.id,
            "date": str(self.event.date)
        }
        serializer = EventSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        event = serializer.save()
        self.assertEqual(event.sport, self.sport)
        self.assertEqual(event.lieu, self.lieu)


# *****************************
# TESTS API
# *****************************
class EventAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.sport = Sport.objects.create(
            nom="Tennis",
            description="Sport de raquette"
        )
        self.lieu = Lieu.objects.create(
            nom="Court central",
            description="Terrain principal",
            code_postal="31000",
            ville="Toulouse"
        )
        self.date = timezone.now().date()

        self.event = Event.objects.create(
            sport=self.sport,
            lieu=self.lieu,
            date=self.date
        )

    def test_list_events(self):
        # test que GET renvoi bien une liste
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_event(self):
        # test de récupération d'un event par son ID
        response = self.client.get(f"/api/events/{self.event.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.event.id)

    def test_create_event(self):
        # test création d'un nouvel event
        data = {
            "sport": self.sport.id,
            "lieu": self.lieu.id,
            "date": str(self.date)
        }
        response = self.client.post("/api/events/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_update_event(self):
        # test la modification d'nu event
        new_date = timezone.now().date()
        data = {
            "sport": self.sport.id,
            "lieu": self.lieu.id,
            "date": str(new_date)
        }
        response = self.client.put(f"/api/events/{self.event.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.date, new_date)

    def test_delete_event(self):
        # test la suppression d'un event
        response = self.client.delete(f"/api/events/{self.event.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_filter_events_by_sport(self):
        # test du filtre par sport
        response = self.client.get(f"/api/events/?sport={self.sport.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
