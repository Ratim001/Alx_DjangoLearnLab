# api/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer # Assuming you have a BookSerializer

# --- Combined List and Create View ---
class BookListCreateView(generics.ListCreateAPIView):
    """
    Handles GET (list books) and POST (create a new book).
    Permission: Read-only for unauthenticated users, create for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Allows anyone to read (GET), but only authenticated users to create (POST)
    permission_classes = [IsAuthenticatedOrReadOnly] 

# --- Combined Detail, Update, and Delete View ---
class BookDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET (retrieve detail), PUT/PATCH (update), and DELETE (destroy/delete).
    Permission: Read-only for unauthenticated, full access for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Allows anyone to read (GET), but only authenticated users to update/delete
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # You can customize behavior here, e.g., perform checks before deletion.
    # def perform_destroy(self, instance):
    #     # Custom logic before deleting the book
    #     instance.delete()