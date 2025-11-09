book = Book.objects.get(id=1)
book.delete()
Book.objects.all()
# <QuerySet []>
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.delete()
Book.objects.all()
# <QuerySet []>
