from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

from .forms import SearchForm

def search_books(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data["q"]
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.none()

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form
    })
