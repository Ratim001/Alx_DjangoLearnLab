from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class SmokeTests(APITestCase):
    def test_test_runner_is_working(self):
        self.assertEqual(status.HTTP_200_OK, 200)
