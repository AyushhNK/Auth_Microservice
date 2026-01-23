from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterViewTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")  
        # example: path("register/", RegisterView.as_view(), name="register")

    def test_register_success(self):
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass@123",
            "password2": "StrongPass@123",
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_password_mismatch(self):
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass@123",
            "password2": "WrongPass@123",
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_duplicate_username(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass@123"
        )

        payload = {
            "username": "testuser",
            "email": "another@example.com",
            "password": "StrongPass@123",
            "password2": "StrongPass@123",
        }

        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.login_url = reverse("login")  
        # example: path("login/", LoginView.as_view(), name="login")

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass@123"
        )

    def test_login_success(self):
        payload = {
            "username": "testuser",
            "password": "StrongPass@123"
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        payload = {
            "username": "testuser",
            "password": "WrongPass"
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        payload = {
            "username": "testuser"
        }

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
