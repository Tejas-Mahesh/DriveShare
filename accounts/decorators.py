from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.core.exceptions import PermissionDenied


def profile_complete_required(view_func):

    def wrapper(request, *args, **kwargs):

        user = request.user

        if user.user_type == "customer":

            if not user.customer_profile.profile_completed:

                messages.warning(
                    request,
                    "Please complete your profile first."
                )

                return redirect("customer_profile")

        elif user.user_type == "owner":

            if not user.owner_profile.profile_completed:

                messages.warning(
                    request,
                    "Please complete your profile first."
                )

                return redirect("owner_profile")

        return view_func(request, *args, **kwargs)

    return wrapper

def approved_owner_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.owner_profile.verification_status != "Approved":

            messages.error(
                request,
                "Your account must be approved before you can add cars."
            )

            return redirect("owner_dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


def approved_customer_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.customer_profile.verification_status != "Approved":

            messages.error(
                request,
                "Your account must be approved before booking cars."
            )

            return redirect("customer_dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


def customer_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            return redirect("login")

        if request.user.user_type != "customer":

            messages.error(request, "Access denied.")

            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


def owner_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            return redirect("login")

        if request.user.user_type != "owner":

            messages.error(request, "Access denied.")

            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            return redirect("login")

        if request.user.user_type != "admin":

            messages.error(request, "Access denied.")

            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper