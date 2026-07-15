from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import profile_complete_required

@login_required(login_url='login')
def customer_dashboard(request):

    if request.user.user_type != "customer":
        return redirect("home")

    return render(
        request,
        "dashboard/customer_dashboard.html"
    )


@login_required(login_url='login')
def owner_dashboard(request):

    if request.user.user_type != "owner":
        return redirect("home")

    return render(
        request,
        "dashboard/owner_dashboard.html"
    )
@login_required(login_url="login")
@profile_complete_required
def customer_dashboard(request):

    if request.user.user_type != "customer":
        return redirect("home")

    return render(
        request,
        "dashboard/customer_dashboard.html"
    )


@login_required(login_url="login")
@profile_complete_required
def owner_dashboard(request):

    if request.user.user_type != "owner":
        return redirect("home")

    return render(
        request,
        "dashboard/owner_dashboard.html"
    )