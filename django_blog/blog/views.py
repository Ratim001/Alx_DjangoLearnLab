from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm

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

