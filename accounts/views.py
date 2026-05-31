from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, ProfileForm, UserCreateForm, UserEditForm

User = get_user_model()


class AppLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


@login_required
def app_logout(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile.html", {"form": form})


def _check_manage(request):
    try:
        return request.user.profile.can_manage_users
    except Exception:
        return False


@login_required
def user_list(request):
    if not _check_manage(request):
        messages.error(request, "Accès refusé.")
        return redirect("incidents:list")
    users = User.objects.select_related("profile").order_by("profile__direction", "username")
    return render(request, "accounts/user_list.html", {"users": users})


@login_required
def user_create(request):
    if not _check_manage(request):
        messages.error(request, "Accès refusé.")
        return redirect("incidents:list")
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Utilisateur « {user.username} » créé.")
            return redirect("accounts:user_list")
    else:
        form = UserCreateForm()
    return render(request, "accounts/user_form.html", {"form": form, "mode": "create"})


@login_required
def user_edit(request, pk):
    if not _check_manage(request):
        messages.error(request, "Accès refusé.")
        return redirect("incidents:list")
    target = get_object_or_404(User, pk=pk)
    profile = target.profile
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=target, profile=profile)
        if form.is_valid():
            form.save()
            form.save_profile(profile)
            messages.success(request, f"Profil de « {target.username} » mis à jour.")
            return redirect("accounts:user_list")
    else:
        form = UserEditForm(instance=target, profile=profile)
    return render(request, "accounts/user_form.html", {"form": form, "target": target, "mode": "edit"})


@login_required
def user_delete(request, pk):
    if not _check_manage(request):
        messages.error(request, "Accès refusé.")
        return redirect("incidents:list")
    target = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        name = target.username
        target.delete()
        messages.success(request, f"Utilisateur « {name} » supprimé.")
        return redirect("accounts:user_list")
    return render(request, "accounts/user_confirm_delete.html", {"target": target})
