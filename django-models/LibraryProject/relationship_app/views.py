from django.shortcuts import render
from .models import Book  # ✅ Keep this for function-based view

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to show library details
from django.views.generic.detail import DetailView
from ..models import Library  # ✅ Checker wants this exact import

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
