from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserTests(TestCase):
    def test_signup(self):
        response = self.client.post(
            reverse("signup"),
            {"username": "testuser", "password1": "myabc123", "password2": "myabc123"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "myabc123"}
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="testuser", password="myabc123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)
