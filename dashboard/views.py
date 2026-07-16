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
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from cars.models import Car
from accounts.models import CustomUser


@login_required
@admin_required
def admin_dashboard(request):

    context = {

        "total_cars": Car.objects.count(),

        "pending_cars": Car.objects.filter(
            approval_status="Pending"
        ).count(),

        "approved_cars": Car.objects.filter(
            approval_status="Approved"
        ).count(),

        "rejected_cars": Car.objects.filter(
            approval_status="Rejected"
        ).count(),

        "total_owners": CustomUser.objects.filter(
            user_type="owner"
        ).count(),

        "total_customers": CustomUser.objects.filter(
            user_type="customer"
        ).count(),

    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context
    )