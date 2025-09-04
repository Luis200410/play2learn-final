from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm, AccountUpdateForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("accounts:account")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def account(request):
    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully.")
            return redirect("accounts:account")
    else:
        form = AccountUpdateForm(instance=request.user)

    return render(request, "accounts/account.html", {"form": form})


def logout_view(request):
    # Log out and return the user to the previous page (or home)
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or reverse("games:home")
    logout(request)
    return redirect(next_url)
