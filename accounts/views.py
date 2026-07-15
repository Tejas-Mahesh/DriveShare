from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    SignUpForm,
    CustomerProfileForm,
    OwnerProfileForm,
    ProfilePictureForm,
)

from .models import CustomerProfile, OwnerProfile
from .decorators import customer_required, owner_required, admin_required


# ==========================
# Signup
# ==========================

def signup(request):

    if request.user.is_authenticated:

        if request.user.user_type == "customer":
            return redirect("customer_dashboard")

        elif request.user.user_type == "owner":
            return redirect("owner_dashboard")

        else:
            return redirect("/admin/")

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()

            if user.user_type == "customer":
                CustomerProfile.objects.create(user=user)

            elif user.user_type == "owner":
                OwnerProfile.objects.create(user=user)

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect("login")

    else:

        form = SignUpForm()

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form
        }
    )


# ==========================
# Login
# ==========================

def login_view(request):

    if request.user.is_authenticated:

        if request.user.user_type == "customer":
            return redirect("customer_dashboard")

        elif request.user.user_type == "owner":
            return redirect("owner_dashboard")

        else:
            return redirect("/admin/")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.user_type == "customer":
                return redirect("customer_dashboard")

            elif user.user_type == "owner":
                return redirect("owner_dashboard")

            else:
                return redirect("/admin/")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "accounts/login.html")


# ==========================
# Logout
# ==========================

def logout_view(request):

    logout(request)

    return redirect("home")


# ==========================
# Customer Profile
# ==========================

@login_required
@customer_required
def customer_profile(request):

    profile = request.user.customer_profile

    if request.method == "POST":

        form = CustomerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        picture_form = ProfilePictureForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid() and picture_form.is_valid():

            profile = form.save(commit=False)
            profile.profile_completed = True
            profile.save()

            picture_form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("customer_dashboard")

    else:

        form = CustomerProfileForm(
            instance=profile
        )

        picture_form = ProfilePictureForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/customer_profile.html",
        {
            "form": form,
            "picture_form": picture_form,
        }
    )


# ==========================
# Owner Profile
# ==========================

@login_required
@owner_required
def owner_profile(request):

    profile = request.user.owner_profile

    if request.method == "POST":

        form = OwnerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        picture_form = ProfilePictureForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid() and picture_form.is_valid():

            profile = form.save(commit=False)
            profile.profile_completed = True
            profile.save()

            picture_form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("owner_dashboard")

    else:

        form = OwnerProfileForm(
            instance=profile
        )

        picture_form = ProfilePictureForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/owner_profile.html",
        {
            "form": form,
            "picture_form": picture_form,
        }
    )