# api/urls.py

from django.urls import path
from .views import BookListCreateView, BookDetailUpdateDeleteView

urlpatterns = [
    # GET: List all books | POST: Create a new book
    path('books/', BookListCreateView.as_view(), name='book-list-create'), 
    
    # GET: Retrieve detail | PUT/PATCH: Update | DELETE: Delete
    path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-detail-update-delete'),
]
