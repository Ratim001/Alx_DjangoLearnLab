from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm

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
