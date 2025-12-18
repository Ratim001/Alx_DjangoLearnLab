# social_media_api/posts/serializers.py
from django.contrib.auth import get_user_model
# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    # Use SerializerMethodField to avoid N+1 queries - counts will be annotated in the view
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "author", "author_username",
            "title", "content", "created_at", "updated_at",
            "likes_count", "comments_count",
        ]
        read_only_fields = ["author", "created_at", "updated_at", "likes_count", "comments_count"]

    def get_likes_count(self, obj):
        # Return annotated count if available, otherwise default to 0
        # Annotation should always be present when using PostViewSet
        return getattr(obj, 'likes_count', 0)
    
    def get_comments_count(self, obj):
        # Return annotated count if available, otherwise default to 0
        # Annotation should always be present when using PostViewSet
        return getattr(obj, 'comments_count', 0)

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_username", "content", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["user", "created_at"]
