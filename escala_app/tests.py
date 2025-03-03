from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class FirebaseLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_without_token(self):
        """Testa login sem fornecer token do Firebase."""
        response = self.client.post("/api/auth/login/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_token(self):
        """Testa login com token inválido."""
        response = self.client.post("/api/auth/login/", {"idToken": "token_invalido"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
