from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import profile_complete_required
from django.db.models import Avg, Count
from bookings.models import Review, Booking
from bookings.models import Wallet
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from bookings.models import Payment
from bookings.models import Booking
from notifications.models import Notification
from cars.models import Wishlist
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from bookings.models import Payment
from decimal import Decimal
@login_required(login_url='login')
def customer_dashboard(request):

    if request.user.user_type != "customer":
        return redirect("home")
    wallet, created = Wallet.objects.get_or_create(
    customer=request.user
)   
    total_bookings = Booking.objects.filter(
    customer=request.user
).count()

    total_notifications = Notification.objects.filter(
    user=request.user
).count()

    total_favorites = Wishlist.objects.filter(
    customer=request.user
).count()
    profile = request.user.customer_profile

    profile_completion = 0

    if request.user.first_name:
        profile_completion += 20

    if request.user.phone_number:
        profile_completion += 20

    if profile.address:
        profile_completion += 20

    if profile.aadhaar_photo:
        profile_completion += 20

    if request.user.profile_picture:
        profile_completion += 20

    return render(
    request,
    "dashboard/customer_dashboard.html",
    {
        "wallet": wallet,
        "total_bookings": total_bookings,
        "total_notifications": total_notifications,
        "total_favorites": total_favorites,
        "profile_completion": profile_completion,
    }
)



from django.db.models import Avg, Sum
from decimal import Decimal

@login_required(login_url="login")
@profile_complete_required
def owner_dashboard(request):

    if request.user.user_type != "owner":
        return redirect("home")

    # ============================
    # Cars
    # ============================

    total_cars = Car.objects.filter(
        owner=request.user
    ).count()

    # ============================
    # Bookings
    # ============================

    total_bookings = Booking.objects.filter(
        car__owner=request.user
    ).count()

    completed_rentals = Booking.objects.filter(
        car__owner=request.user,
        booking_status="Completed"
    ).count()

    # ============================
    # Reviews
    # ============================

    owner_reviews = Review.objects.filter(
        car__owner=request.user
    )

    owner_rating = owner_reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    owner_review_count = owner_reviews.count()

    # ============================
    # Earnings
    # ============================

    total_earnings = Payment.objects.filter(
        booking__car__owner=request.user,
        payment_status="Paid"
    ).aggregate(
        total=Sum("owner_amount")
    )["total"] or Decimal("0.00")

    # ============================
    # Context
    # ============================

    context = {

        "total_cars": total_cars,

        "total_bookings": total_bookings,

        "total_earnings": total_earnings,

        "owner_rating": owner_rating,

        "owner_review_count": owner_review_count,

        "completed_rentals": completed_rentals,

    }

    return render(
        request,
        "dashboard/owner_dashboard.html",
        context,
    )
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from cars.models import Car
from accounts.models import CustomUser


@login_required
@admin_required
def admin_dashboard(request):

    # ===============================
    # Dashboard Statistics
    # ===============================

    total_cars = Car.objects.count()

    pending_cars = Car.objects.filter(
        approval_status="Pending"
    ).count()

    approved_cars = Car.objects.filter(
        approval_status="Approved"
    ).count()

    rejected_cars = Car.objects.filter(
        approval_status="Rejected"
    ).count()

    total_owners = CustomUser.objects.filter(
        user_type="owner"
    ).count()

    total_customers = CustomUser.objects.filter(
        user_type="customer"
    ).count()

    # ===============================
    # Monthly Booking Chart
    # ===============================

    monthly_bookings = (
        Booking.objects
        .annotate(month=TruncMonth("booked_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    booking_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_bookings
    ]

    booking_counts = [
        item["total"]
        for item in monthly_bookings
    ]

    # ===============================
    # Monthly Revenue Chart
    # ===============================

    monthly_revenue = (
        Payment.objects.filter(
            payment_status="Paid"
        )
        .annotate(month=TruncMonth("paid_at"))
        .values("month")
        .annotate(revenue=Sum("amount"))
        .order_by("month")
    )

    revenue_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_revenue
    ]

    revenue_values = [
        float(item["revenue"] or 0)    
        for item in monthly_revenue
    ]

    paid_count = Payment.objects.filter(
    payment_status="Paid"
).count()

    pending_count = Payment.objects.filter(
    payment_status="Pending"
).count()

    failed_count = Payment.objects.filter(
    payment_status="Failed"
).count()

    refunded_count = Payment.objects.filter(
    payment_status="Refunded"
).count()

    # ===============================
    # Context
    # ===============================

    context = {

        "total_cars": total_cars,

        "pending_cars": pending_cars,

        "approved_cars": approved_cars,

        "rejected_cars": rejected_cars,

        "total_owners": total_owners,

        "total_customers": total_customers,

        "booking_labels": booking_labels,

        "booking_counts": booking_counts,

        "revenue_labels": revenue_labels,

        "revenue_values": revenue_values,
        "payment_status_labels": [
    "Paid",
    "Pending",
    "Failed",
    "Refunded",
],

"payment_status_data": [
    paid_count,
    pending_count,
    failed_count,
    refunded_count,
],

    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context,
    )
def about(request):

    return render(
        request,
        "core/about.html",
    )
def contact(request):

    return render(
        request,
        "core/contact.html",
    )
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")

        email = request.POST.get("email")

        subject = request.POST.get("subject")

        message = request.POST.get("message")

        full_message = f"""
New Contact Form Submission

Name: {name}

Email: {email}

Subject: {subject}

Message:

{message}
"""

        send_mail(
            subject=f"DriveShare Contact - {subject}",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        messages.success(
            request,
            "Thank you! Your message has been sent successfully."
        )

        return redirect("contact")

    return render(
        request,
        "core/contact.html"
    )

@login_required
def revenue_report(request):

    if not request.user.is_superuser:
        return redirect("home")

    today = timezone.now().date()

    daily_revenue = (
        Payment.objects.filter(
            payment_status="Paid",
            paid_at__date=today
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    monthly_revenue = (
        Payment.objects.filter(
            payment_status="Paid",
            paid_at__year=today.year,
            paid_at__month=today.month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    yearly_revenue = (
        Payment.objects.filter(
            payment_status="Paid",
            paid_at__year=today.year
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    commission = yearly_revenue * Decimal(0.10)

    context = {
        "daily_revenue": daily_revenue,
        "monthly_revenue": monthly_revenue,
        "yearly_revenue": yearly_revenue,
        "commission": commission,
    }

    return render(
        request,
        "dashboard/revenue_report.html",
        context,
    )
