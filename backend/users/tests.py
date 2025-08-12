from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    # Test la creation d'un user
    def test_user_registration(self):
        data = {
            "username": "testuser",
            "first_name": "Test",
            "email": "testuser@example.com",
            "password": "Testpass123!",
            "password2": "Testpass123!"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    # test le login
    def test_user_login(self):
        self.test_user_registration()

        login_data = {
            "username": "testuser",
            "password": "Testpass123!"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

