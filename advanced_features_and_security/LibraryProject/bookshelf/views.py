from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Add select_related if Book has foreign keys to optimize queries
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

from .forms import SearchForm

def search_books(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data["q"]
        # Add select_related if Book has foreign keys to optimize queries
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.none()

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form
    })


from django.shortcuts import render
from .forms import ExampleForm

def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            return render(request, "bookshelf/form_example.html", {"form": form, "title": title})
    else:
        form = ExampleForm()

    return render(request, "bookshelf/form_example.html", {"form": form})
