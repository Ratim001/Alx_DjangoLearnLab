from django.urls import path
from .views import BookList  # or import book_list if using function view

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    # if function view used: path('books/', book_list, name='book-list'),
]
