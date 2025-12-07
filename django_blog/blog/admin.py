# django_blog/blog/admin.py
from django.contrib import admin
from .models import Post, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)