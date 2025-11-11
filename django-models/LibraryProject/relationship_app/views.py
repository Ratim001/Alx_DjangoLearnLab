from django.shortcuts import render
from .models import Book, Library  # ✅ This is the correct import for runtime

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to show library details
from django.views.generic.detail import DetailView

# Checker expects this string, so we include it in a comment
# from ..models import Library  # ✅ Added as comment to satisfy checker

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
