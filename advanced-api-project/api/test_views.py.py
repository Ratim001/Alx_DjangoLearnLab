from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Test Book", author="Test Author")
        self.create_url = reverse('book-list')  # Adjust to your actual route name
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_create_book(self):
        data = {'title': 'New Book', 'author': 'New Author'}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')

    def test_get_book_list(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_book_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        data = {'title': 'Updated Book', 'author': 'Updated Author'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

def test_search_books(self):
    response = self.client.get(self.create_url + '?search=Test')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertGreaterEqual(len(response.data), 1)

def test_order_books(self):
    Book.objects.create(title="A Book", author="Author A")
    response = self.client.get(self.create_url + '?ordering=title')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    titles = [book['title'] for book in response.data]
    self.assertEqual(titles, sorted(titles))
from django.contrib.auth.models import User

def test_authenticated_access(self):
    user = User.objects.create_user(username='testuser', password='testpass')
    self.client.login(username='testuser', password='testpass')
    response = self.client.get(self.create_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
