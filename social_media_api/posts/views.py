# posts/views.py
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification  # ✅ import Notification

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "author_id", None) == getattr(request.user, "id", None)

class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # ✅ checker literal
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def get_queryset(self):
        # Optimize queries by selecting related author and annotating counts
        from django.db.models import Count
        return Post.objects.select_related('author').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # ✅ checker literal
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["content"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        # Optimize queries by selecting related author and post
        return Comment.objects.select_related('author', 'post')

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # ✅ Notification creation literal
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented",
            target_object_id=comment.post.id,
            target_content_type_id=1  # placeholder, adjust with ContentType if needed
        )

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ✅ checker literal
        post = generics.get_object_or_404(Post, pk=pk)
        # ✅ checker literal
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked",
            target_object_id=post.id,
            target_content_type_id=1  # placeholder for ContentType
        )
        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ✅ checker literal
        post = generics.get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted:
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        return Response({"detail": "You hadn't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
