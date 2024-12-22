from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app.models import Document


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
        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout(self):
        self.client.login(username="testuser", password="myabc123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)


class DocumentUploadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="myabc123")

    def test_document_upload(self):
        self.client.login(username="testuser", password="myabc123")
        with open("testfile.txt", "w") as file:
            file.write("Sample content")
        with open("testfile.txt", "rb") as file:
            response = self.client.post(reverse("upload_document"), {"document": file})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Document.objects.filter(
                user=self.user, document_name="testfile.txt"
            ).exists()
        )


class ChatbotViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="myabc123")
        Document.objects.create(user=self.user, document_name="testdoc.txt")

    def test_chatbot_view(self):
        self.client.login(username="testuser", password="myabc123")
        response = self.client.get(reverse("chatbot"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "testdoc.txt"
        )  # Document is displayed in the chatbot view
