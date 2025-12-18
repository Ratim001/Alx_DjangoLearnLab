from django.db import models

# Create your models here.from django.db import models

# Author model: represents a writer with a name
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Book model: represents a book linked to an author
class Book(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    class Meta:
        # Add indexes for frequently searched/filtered fields to improve performance
        indexes = [
            models.Index(fields=['title']),  # For title searches
            models.Index(fields=['author']),  # For filtering by author
            models.Index(fields=['publication_year']),  # For year filtering
            models.Index(fields=['author', 'publication_year']),  # Combined filter
        ]

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # or IsAuthenticatedOrReadOnly if you want stricter rules

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']   # ✅ search by author name
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering

    def get_queryset(self):
        # Optimize queries by selecting related author to avoid N+1 queries
        return Book.objects.select_related('author')
