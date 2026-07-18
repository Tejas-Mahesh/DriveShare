from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import profile_complete_required
from django.db.models import Avg, Count
from bookings.models import Review, Booking
from bookings.models import Wallet
@login_required(login_url='login')
def customer_dashboard(request):

    if request.user.user_type != "customer":
        return redirect("home")
    wallet, created = Wallet.objects.get_or_create(
    customer=request.user
)

    return render(
        request,
        "dashboard/customer_dashboard.html",{
            "wallet":wallet,

        }
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
    owner_reviews = Review.objects.filter(
    car__owner=request.user
)

    owner_rating = owner_reviews.aggregate(
    Avg("rating")
)["rating__avg"]

    owner_review_count = owner_reviews.count()

    completed_rentals = Booking.objects.filter(
    car__owner=request.user,
    booking_status="Completed"
).count()

    return render(
        request,
        "dashboard/owner_dashboard.html",{
             "owner_rating": owner_rating,
        "owner_review_count": owner_review_count,
        "completed_rentals": completed_rentals,


        }
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

