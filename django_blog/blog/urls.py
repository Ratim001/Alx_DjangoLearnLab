# django_blog/blog/urls.py
from django.urls import path
from .views import UserLoginView, UserLogoutView, register, profile

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]
