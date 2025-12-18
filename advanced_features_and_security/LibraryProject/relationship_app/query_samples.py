from relationship_app.models import Author, Book, Library, Librarian
from django.core.exceptions import ObjectDoesNotExist

# Query all books by a specific author
def books_by_author(author_name):
    """
    Optimized: Use filter instead of get to avoid exceptions
    Returns books by author efficiently
    """
    try:
        author = Author.objects.get(name=author_name)
        # Optimize by selecting related author data
        return Book.objects.filter(author=author).select_related('author')
    except ObjectDoesNotExist:
        return Book.objects.none()

# List all books in a library
def books_in_library(library_name):
    """
    Optimized: Use prefetch_related to avoid N+1 queries on books
    """
    try:
        library = Library.objects.prefetch_related('books').get(name=library_name)
        return library.books.all()
    except ObjectDoesNotExist:
        return Book.objects.none()

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    """
    Optimized: Use select_related to get library data efficiently
    """
    try:
        library = Library.objects.get(name=library_name)
        return Librarian.objects.select_related('library').get(library=library)
    except ObjectDoesNotExist:
        return None
