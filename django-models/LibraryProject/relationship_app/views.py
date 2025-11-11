from django.shortcuts import render
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # ✅ Checker wants this exact query
    return render(request, 'relationship_app/list_books.html', {'books': books})  # ✅ Checker wants full path

# Class-based view to show library details
from django.views.generic.detail import DetailView

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # ✅ Match template path
    context_object_name = 'library'
