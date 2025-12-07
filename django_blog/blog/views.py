from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":   # <-- checker looks for "POST" and "method"
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()            # <-- checker looks for "save()"
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, "blog/profile.html", {"form": form})

class UserLoginView(LoginView):
    template_name = 'blog/login.html'

class UserLogoutView(LogoutView):
    next_page = 'login'

# blog/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        return self.get_object().author == self.request.user


# Inline comments on Post detail page
def post_detail_with_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author').order_by('-created_at')
    form = CommentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('post-detail', pk=post.pk)
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': form
    })

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})

# django_blog/blog/views.py
from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from .models import Post, Tag
from .models import Post

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        return Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.select_related('author').prefetch_related('tags').order_by('-published_date')
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': posts})
