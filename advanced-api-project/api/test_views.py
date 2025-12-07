from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Book


class SmokeTests(APITestCase):
    def test_test_runner_is_working(self):
        self.assertEqual(status.HTTP_200_OK, 200)

User = get_user_model()

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username="tester", password="pass1234")
        self.client.force_authenticate(user=self.user)

        # Create a book in the test database
        self.book = Book.objects.create(
            title="Test Driven Django",
            author="Jane Doe",
            published_date="2025-01-01",
            price=20.00,
            owner=self.user
        )

        self.list_url = reverse("book-list")  # adjust if your router name differs

    def test_list_books_returns_data_and_status_code(self):
        response = self.client.get(self.list_url)
        # ✅ Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Check response.data exists
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)
        # ✅ Inspect fields
        first = response.data[0]
        self.assertIn("title", first)
        self.assertIn("author", first)
