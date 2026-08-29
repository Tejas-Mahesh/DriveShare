from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from accounts.decorators import customer_required
from cars.models import Car
from .forms import BookingForm
from .models import Booking
from django.db.models import Q
from django.db.models import Sum, Count
from accounts.models import CustomUser
from cars.models import Car
from .models import Review
from .forms import ReviewForm
from django.db.models import Avg, Count
from cars.models import Car
from accounts.models import CustomUser
from .models import Payment
import razorpay
from django.conf import settings
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
import json
from notifications.utils import create_notification
from .models import Booking, Review, Payment, Wallet, WalletTransaction
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import customer_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from datetime import timedelta

from cars.models import Car
from .models import Booking, Payment

import base64
import qrcode

from io import BytesIO
from urllib.parse import urlencode
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.decorators import customer_required
from accounts.models import CustomUser, OwnerProfile

from .models import (
    Booking,
    Payment,
    Wallet,
    WalletTransaction,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Booking
from .forms import BookingForm
from cars.models import Car
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from urllib.parse import urlencode

from django.db import transaction

@login_required
def book_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        approval_status="Approved",
        is_available=True
    )

    # Existing approved bookings
    approved_bookings = Booking.objects.filter(
        car=car,
        booking_status="Approved"
    ).order_by("start_date")

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            # Check that start date isn't in the past
            if start_date < timezone.localdate():

                form.add_error(
                    "start_date",
                    "Start date cannot be in the past."
                )

            else:

                # Check date overlap
                overlapping_booking = Booking.objects.filter(
                    car=car,
                    booking_status="Approved",
                    start_date__lt=end_date,
                    end_date__gt=start_date
                ).exists()

                if overlapping_booking:

                    form.add_error(
                        None,
                        "The selected dates are already booked."
                    )

                else:

                    total_days = (
                        end_date - start_date
                    ).days

                    total_amount = (
                        total_days * car.price_per_day
                    )

                    with transaction.atomic():
                        booking = form.save(commit=False)
                        booking.customer = request.user
                        booking.car = car
                        booking.total_days = total_days
                        booking.total_amount = total_amount
                        booking.booking_status = "Pending"
                        booking.save()

                        Payment.objects.create(
                            booking=booking,
                            customer=request.user,
                            amount=total_amount,
                            payment_status="Pending"
                        )

                    messages.success(
                        request,
                        "Booking request submitted successfully."
                    )

                    return redirect(
                        "booking_details",
                        booking_id=booking.id
                    )

    else:

        form = BookingForm()

    return render(
        request,
        "bookings/book_car.html",
        {
            "form": form,
            "car": car,
            "approved_bookings": approved_bookings,
        }
    )
@login_required
@customer_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related(
        "car"
    ).order_by("-booked_at")

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:

        bookings = bookings.filter(

            Q(car__title__icontains=search) |
            Q(car__brand__icontains=search) |
            Q(car__model__icontains=search)

        )

    if status:

        bookings = bookings.filter(
            booking_status=status
        )

    paginator = Paginator(bookings, 6)

    page_number = request.GET.get("page")

    bookings = paginator.get_page(page_number)

    return render(
        request,
        "bookings/my_bookings.html",
        {
            "bookings": bookings,
            "search": search,
            "status": status,
        }
    )
from django.utils import timezone
from django.shortcuts import get_object_or_404, render

@login_required
@customer_required
def booking_details(request, booking_id):

    booking = get_object_or_404(
        Booking.objects.select_related(
            "car",
            "car__owner",
            "customer",
        ),
        id=booking_id,
        customer=request.user,
    )

    today = timezone.localdate()

    payment = getattr(
        booking,
        "payment",
        None
    )

    # ---------------------------------------------
    # AUTOMATIC RENTAL START
    # ---------------------------------------------

    rental_started = False

    if (
        booking.booking_status in [
            "Approved",
            "Completed"
        ]
        and payment
        and payment.payment_status == "Paid"
        and booking.start_date <= today
    ):
        rental_started = True

    # ---------------------------------------------
    # AUTOMATIC RENTAL COMPLETION
    # ---------------------------------------------

    if (
        booking.booking_status == "Approved"
        and payment
        and payment.payment_status == "Paid"
        and booking.end_date < today
    ):

        booking.booking_status = "Completed"

        if not booking.completed_at:
            booking.completed_at = timezone.now()

        booking.save(
            update_fields=[
                "booking_status",
                "completed_at",
                "updated_at",
            ]
        )

    # ---------------------------------------------
    # PAYMENT STATE
    # ---------------------------------------------

    payment_paid = (
        payment
        and payment.payment_status == "Paid"
    )

    payment_pending = (
        payment
        and payment.payment_status == "Pending"
    )

    payment_failed = (
        payment
        and payment.payment_status == "Failed"
    )

    return render(
        request,
        "bookings/booking_details.html",
        {
            "booking": booking,
            "payment": payment,
            "payment_paid": payment_paid,
            "payment_pending": payment_pending,
            "payment_failed": payment_failed,
            "rental_started": rental_started,
            "today": today,
        },
    )
@login_required
@customer_required
def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user,
    )

    # ---------------------------------------------
    # ONLY PENDING BOOKING CAN BE CANCELLED
    # ---------------------------------------------

    if booking.booking_status != "Pending":

        messages.error(
            request,
            "This booking cannot be cancelled."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    booking.booking_status = "Cancelled"

    booking.save(
        update_fields=[
            "booking_status",
            "updated_at",
        ]
    )

    create_notification(
        user=booking.car.owner,
        title="Booking Cancelled",
        message=(
            f"{booking.customer.get_full_name()} "
            f"or {booking.customer.username} "
            f"cancelled the booking for "
            f"{booking.car.title}."
        ),
        notification_type="Booking",
        redirect_url="/bookings/owner-bookings/",
    )

    messages.success(
        request,
        "Booking cancelled successfully."
    )

    return redirect(
        "my_bookings"
    )
from django.shortcuts import get_object_or_404
from accounts.decorators import owner_required


from django.core.paginator import Paginator
from django.db.models import Q


@login_required
@owner_required
def owner_bookings(request):

    bookings = Booking.objects.filter(
        car__owner=request.user
    ).select_related(
        "customer",
        "car"
    ).order_by("-booked_at")

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:

        bookings = bookings.filter(

            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(customer__username__icontains=search) |
            Q(car__title__icontains=search) |
            Q(car__brand__icontains=search)

        )

    if status:

        bookings = bookings.filter(
            booking_status=status
        )

    paginator = Paginator(bookings, 6)

    page = request.GET.get("page")

    bookings = paginator.get_page(page)
    total_bookings = Booking.objects.filter(
    car__owner=request.user
).count()

    pending_bookings = Booking.objects.filter(
    car__owner=request.user,
    booking_status="Pending"
).count()

    approved_bookings = Booking.objects.filter(
    car__owner=request.user,
    booking_status="Approved"
).count()

    rejected_bookings = Booking.objects.filter(
    car__owner=request.user,
    booking_status="Rejected"
).count()

    approved_amount = Booking.objects.filter(
    car__owner=request.user,
    booking_status="Approved"
)

    expected_earnings = sum(
    booking.total_amount
    for booking in approved_amount
)
    payment_pending_count = Booking.objects.filter(
    car__owner=request.user,
    booking_status="Approved",
    payment__payment_status="Pending"
).count()

    return render(
    request,
    "bookings/owner_bookings.html",
    {
        "bookings": bookings,
        "search": search,
        "status": status,

        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "approved_bookings": approved_bookings,
        "rejected_bookings": rejected_bookings,
        "expected_earnings": expected_earnings,
    }
)
@login_required
@owner_required
def owner_booking_details(request, booking_id):

    booking = get_object_or_404(
        Booking.objects.select_related(
            "customer",
            "car",
            "car__owner",
            "payment",
        ),
        id=booking_id,
        car__owner=request.user,
    )

    payment = getattr(
        booking,
        "payment",
        None
    )

    return render(
        request,
        "bookings/owner_booking_details.html",
        {
            "booking": booking,
            "payment": payment,
        }
    )
from notifications.models import Notification
@login_required
@owner_required
def approve_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__owner=request.user
    )

    if booking.booking_status != "Pending":

        messages.warning(
            request,
            "Only pending bookings can be approved."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    conflict = Booking.objects.filter(
        car=booking.car,
        booking_status="Approved",
        start_date__lt=booking.end_date,
        end_date__gt=booking.start_date,
    ).exclude(
        id=booking.id
    ).exists()

    if conflict:

        messages.error(
            request,
            "This car is already booked for these dates."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    booking.booking_status = "Approved"
    booking.approved_at = timezone.now()

    booking.save(
        update_fields=[
            "booking_status",
            "approved_at",
            "updated_at",
        ]
    )

    create_notification(
        user=booking.customer,
        title="Booking Approved",
        message=(
            f"Your booking for "
            f"{booking.car.title} has been approved. "
            f"You can now make the payment."
        ),
        notification_type="Booking",
        redirect_url=(
            f"/bookings/details/{booking.id}/"
        ),
    )

    messages.success(
        request,
        "Booking approved successfully."
    )

    return redirect(
        "owner_booking_details",
        booking.id
    )
@login_required
@owner_required
def reject_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__owner=request.user
    )

    if booking.booking_status != "Pending":

        messages.warning(
            request,
            "Only pending bookings can be rejected."
        )

        return redirect(
            "owner_bookings"
        )

    booking.booking_status = "Rejected"

    booking.save(
        update_fields=[
            "booking_status",
            "updated_at",
        ]
    )

    create_notification(
        user=booking.customer,
        title="Booking Rejected",
        message=(
            f"Your booking for "
            f"{booking.car.title} has been rejected."
        ),
        notification_type="Booking",
        redirect_url=(
            f"/bookings/details/{booking.id}/"
        ),
    )

    messages.success(
        request,
        "Booking rejected successfully."
    )

    return redirect(
        "owner_booking_details",
        booking.id
    )
@login_required
@owner_required
def owner_notifications(request):

    notifications = Booking.objects.filter(
        car__owner=request.user
    ).select_related(
        "customer",
        "car"
    ).order_by("-booked_at")

    return render(
        request,
        "bookings/owner_notifications.html",
        {
            "notifications": notifications,
        }
    )
from accounts.decorators import admin_required
from django.core.paginator import Paginator

@login_required
@admin_required
def admin_bookings(request):

    bookings = Booking.objects.select_related(
        "customer",
        "car",
        "car__owner"
    ).order_by("-booked_at")

    total_bookings = bookings.count()

    approved_bookings = bookings.filter(
        booking_status="Approved"
    ).count()

    pending_bookings = bookings.filter(
        booking_status="Pending"
    ).count()

    rejected_bookings = bookings.filter(
        booking_status="Rejected"
    ).count()

    cancelled_bookings = bookings.filter(
        booking_status="Cancelled"
    ).count()

    completed_bookings = bookings.filter(
        booking_status="Completed"
    ).count()

    total_revenue = sum(
        booking.total_amount
        for booking in bookings
        if booking.booking_status in ["Approved", "Completed"]
    )

    commission_rate =  Decimal("0.10")

    platform_commission = total_revenue * commission_rate
    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        bookings = bookings.filter(
        Q(customer__username__icontains=search)
        | Q(customer__first_name__icontains=search)
        | Q(car__title__icontains=search)
        | Q(car__brand__icontains=search)
        | Q(car__owner__username__icontains=search)
    )

    if status:
        bookings = bookings.filter(
        booking_status=status
    )
    paginator = Paginator(bookings, 8)

    page = request.GET.get("page")

    bookings = paginator.get_page(page)
    for booking in bookings:
        booking.commission = booking.total_amount * Decimal("0.10")

        booking.owner_earning = (
        booking.total_amount
        - booking.commission
    )
        
    total_customers = CustomUser.objects.filter(
    user_type="customer"
).count()

    total_owners = CustomUser.objects.filter(
    user_type="owner"
).count()

    total_cars = Car.objects.count()

    from django.db.models import Count

    top_car = Car.objects.annotate(
    booking_count=Count("bookings")
).order_by("-booking_count").first()

    top_owner = CustomUser.objects.filter(
    user_type="owner"
).annotate(
    booking_count=Count("cars__bookings")
).order_by("-booking_count").first()    
    return render(
        request,
        "bookings/admin_bookings.html",
        {
            "bookings": bookings,

            "total_bookings": total_bookings,
            "approved_bookings": approved_bookings,
            "pending_bookings": pending_bookings,
            "rejected_bookings": rejected_bookings,
            "cancelled_bookings": cancelled_bookings,
            "completed_bookings": completed_bookings,

            "total_revenue": total_revenue,
            "platform_commission": platform_commission,
            "search": search,
"status": status,
"total_customers": total_customers,
"total_owners": total_owners,
"total_cars": total_cars,
"top_car": top_car,
"top_owner": top_owner,
        }
    )
@login_required
@admin_required
def admin_booking_details(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )
    commission_rate = Decimal("0.10")

    platform_commission = booking.total_amount * commission_rate

    owner_amount = booking.total_amount - platform_commission

    return render(
    request,
    "bookings/admin_booking_details.html",
    {
        "booking": booking,
        "platform_commission": platform_commission,
        "owner_amount": owner_amount,
    }
)
import csv
from django.http import HttpResponse
@login_required
@admin_required
def export_bookings_csv(request):

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="driveshare_bookings.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Booking ID",
        "Customer",
        "Owner",
        "Car",
        "Start Date",
        "End Date",
        "Total Days",
        "Amount",
        "Status",
        "Booked On",
    ])

    bookings = Booking.objects.select_related(
        "customer",
        "car",
        "car__owner"
    )

    for booking in bookings:

        writer.writerow([
            booking.id,
            booking.customer.get_full_name() or booking.customer.username,
            booking.car.owner.get_full_name() or booking.car.owner.username,
            booking.car.title,
            booking.start_date,
            booking.end_date,
            booking.total_days,
            booking.total_amount,
            booking.booking_status,
            booking.booked_at,
        ])

    return response


@login_required
def add_review(request, booking_id):

    booking = get_object_or_404(

        Booking,

        id=booking_id,

        customer=request.user,

        booking_status="Completed"

    )

    if hasattr(booking, "review"):

        messages.info(
            request,
            "You have already reviewed this booking."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    if request.method == "POST":

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.booking = booking

            review.car = booking.car

            review.customer = request.user

            review.save()

            messages.success(
                request,
                "Thank you for your review!"
            )

            return redirect(
                "booking_details",
                booking.id
            )

    else:

        form = ReviewForm()

    return render(

        request,

        "bookings/add_review.html",

        {

            "form":form,

            "booking":booking

        }

    )
@login_required
@admin_required
def admin_reviews(request):

    reviews = Review.objects.select_related(
        "customer",
        "car",
        "car__owner"
    ).order_by("-created_at")

    search = request.GET.get("search")

    rating = request.GET.get("rating")

    if search:

        reviews = reviews.filter(

            Q(customer__username__icontains=search) |

            Q(customer__first_name__icontains=search) |

            Q(car__title__icontains=search) |

            Q(car__owner__username__icontains=search)

        )

    if rating:

        reviews = reviews.filter(
            rating=rating
        )

    paginator = Paginator(reviews,10)

    page=request.GET.get("page")

    reviews=paginator.get_page(page)

    average_rating = Review.objects.aggregate(
    Avg("rating")
)["rating__avg"]

    total_reviews = Review.objects.count()

    five_star = Review.objects.filter(rating=5).count()
    four_star = Review.objects.filter(rating=4).count()
    three_star = Review.objects.filter(rating=3).count()
    two_star = Review.objects.filter(rating=2).count()
    one_star = Review.objects.filter(rating=1).count()

    top_car = (
    Car.objects.annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews")
    )
    .order_by("-avg_rating", "-review_count")
    .first()
)

    top_owner = (
    CustomUser.objects.filter(user_type="owner")
    .annotate(
        avg_rating=Avg("cars__reviews__rating"),
        review_count=Count("cars__reviews")
    )
    .order_by("-avg_rating", "-review_count")
    .first()
)

    return render(

        request,

        "bookings/admin_reviews.html",

        {

            "reviews":reviews,

            "search":search,

            "rating":rating,
            "average_rating": average_rating,
"total_reviews": total_reviews,

"five_star": five_star,
"four_star": four_star,
"three_star": three_star,
"two_star": two_star,
"one_star": one_star,

"top_car": top_car,
"top_owner": top_owner,

        }

    )
@login_required
@admin_required
def delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id
    )

    review.delete()

    messages.success(
        request,
        "Review deleted successfully."
    )

    return redirect(
        "admin_reviews"
    )

@login_required
@owner_required
def complete_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__owner=request.user,
    )

    today = timezone.localdate()

    if booking.booking_status != "Approved":

        messages.error(
            request,
            "Only approved bookings can be completed."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    payment = getattr(
        booking,
        "payment",
        None
    )

    if not payment or payment.payment_status != "Paid":

        messages.error(
            request,
            "Booking cannot be completed until payment is verified."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    if booking.end_date >= today:

        messages.error(
            request,
            "Rental can only be completed after the end date."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    booking.booking_status = "Completed"
    booking.completed_at = timezone.now()

    booking.save(
        update_fields=[
            "booking_status",
            "completed_at",
            "updated_at",
        ]
    )

    create_notification(
        user=booking.customer,
        title="Rental Completed",
        message=(
            f"Your rental of "
            f"{booking.car.title} has been completed."
        ),
        notification_type="Booking",
        redirect_url=(
            f"/bookings/details/{booking.id}/"
        ),
    )

    messages.success(
        request,
        "Rental completed successfully."
    )

    return redirect(
        "owner_booking_details",
        booking.id
    )

from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Booking, Payment


@login_required
@customer_required
def payment_page(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    if booking.booking_status != "Approved":

        messages.error(
            request,
            "Payment is available only after owner approval."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            "customer": request.user,
            "amount": booking.total_amount,
            "payment_status": "Pending",
        }
    )

    if payment.payment_status == "Paid":

        messages.info(
            request,
            "This booking has already been paid."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    car = booking.car
    owner = car.owner

    try:
        owner_profile = owner.owner_profile
    except OwnerProfile.DoesNotExist:

        messages.error(
            request,
            "Owner payment details are not available."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    if not owner_profile.upi_id:

        messages.error(
            request,
            "Owner has not added a UPI ID."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    upi_id = owner_profile.upi_id.strip()

    owner_name = (
        owner.get_full_name()
        or owner.username
    )

    amount = payment.amount

    upi_params = {
        "pa": upi_id,
        "pn": owner_name,
        "am": f"{amount:.2f}",
        "cu": "INR",
        "tn": (
            f"DriveShare Booking "
            f"{booking.invoice_number}"
        ),
    }

    upi_url = (
        "upi://pay?"
        + urlencode(upi_params)
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(upi_url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()

    qr_image.save(
        buffer,
        format="PNG"
    )

    qr_image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return render(
        request,
        "bookings/payment.html",
        {
            "booking": booking,
            "car": car,
            "owner": owner,
            "owner_profile": owner_profile,
            "payment": payment,
            "upi_id": upi_id,
            "owner_name": owner_name,
            "upi_url": upi_url,
            "qr_image": qr_image_base64,
        }
    )

@login_required
@customer_required
def payment_failed(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    payment = booking.payment

    payment.payment_status = "Failed"

    payment.save()
    create_notification(
    user=request.user,
    title="Payment Failed",
    message=f"Payment of ₹{payment.amount} could not be completed.",
    notification_type="Payment",
    redirect_url="/bookings/payment-history/",
)

    messages.error(
        request,
        "Payment was cancelled or failed."
    )

    return render(
        request,
        "bookings/payment_failed.html",
        {
            "booking": booking,
            "payment": payment,
        }
    )
from django.db import transaction


@login_required
@customer_required
def wallet_payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    if booking.booking_status != "Approved":

        messages.error(
            request,
            "Payment is available only after owner approval."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    payment = get_object_or_404(
        Payment,
        booking=booking,
        customer=request.user
    )

    if payment.payment_status == "Paid":

        messages.info(
            request,
            "This booking has already been paid."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    try:

        wallet = Wallet.objects.get(
            customer=request.user
        )

    except Wallet.DoesNotExist:

        messages.error(
            request,
            "Wallet not found."
        )

        return redirect(
            "payment_page",
            booking.id
        )

    if wallet.balance < payment.amount:

        messages.error(
            request,
            "Insufficient wallet balance."
        )

        return redirect(
            "payment_page",
            booking.id
        )

    with transaction.atomic():

        wallet.balance -= payment.amount

        wallet.save(
            update_fields=[
                "balance",
                "updated_at",
            ]
        )

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=payment.amount,
            transaction_type="Debit",
            description=(
                f"Payment for Booking #{booking.id}"
            ),
        )

        payment.payment_status = "Paid"
        payment.payment_method = "Wallet"
        payment.paid_at = timezone.now()
        payment.verified_at = timezone.now()
        payment.verified_by = None

        payment.commission = (
            payment.amount * Decimal("10")
        ) / Decimal("100")

        payment.owner_amount = (
            payment.amount
            - payment.commission
        )

        payment.save()

    create_notification(
        user=request.user,
        title="Wallet Payment Successful",
        message=(
            f"₹{payment.amount} was deducted "
            f"from your wallet for Booking "
            f"#{booking.id}."
        ),
        notification_type="Wallet",
        redirect_url="/bookings/wallet/",
    )

    create_notification(
        user=booking.car.owner,
        title="Booking Payment Received",
        message=(
            f"{booking.customer.get_full_name()} "
            f"or {booking.customer.username}"
            f"paid ₹{payment.amount} using wallet "
            f"for {booking.car.title}."
        ),
        notification_type="Payment",
        redirect_url=(
            f"/bookings/owner/details/{booking.id}/"
        ),
    )

    messages.success(
        request,
        "Payment completed using your wallet."
    )

    return redirect(
        "booking_details",
        booking.id
    )
@login_required
@customer_required
def payment_history(request):

    payments = Payment.objects.filter(
        customer=request.user
    ).select_related(
        "booking",
        "booking__car"
    ).order_by("-created_at")

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:

        payments = payments.filter(

            Q(booking__car__title__icontains=search) |

            Q(transaction_id__icontains=search)

        )

    if status:

        payments = payments.filter(
            payment_status=status
        )

    paginator = Paginator(payments, 8)

    page = request.GET.get("page")

    payments = paginator.get_page(page)
    total_payments = Payment.objects.filter(
    customer=request.user
).count()

    paid_payments = Payment.objects.filter(
    customer=request.user,
    payment_status="Paid"
).count()

    failed_payments = Payment.objects.filter(
    customer=request.user,
    payment_status="Failed"
).count()

    total_amount = Payment.objects.filter(
    customer=request.user,
    payment_status="Paid"
).aggregate(
    total=Sum("amount")
)["total"] or 0
    return render(
        request,
        "bookings/payment_history.html",
        {
            "payments": payments,
            "search": search,
            "status": status,
            "total_payments": total_payments,
"paid_payments": paid_payments,
"failed_payments": failed_payments,
"total_amount": total_amount,
        }
    )
@login_required
@customer_required
def download_receipt(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        customer=request.user,
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Receipt_{payment.id}.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()
    invoice_number = f"DS-{payment.id:06d}"

    generated_date = timezone.now().strftime(
    "%d %B %Y %I:%M %p"
)

    commission = payment.amount * Decimal("0.10")

    owner_amount = payment.amount - commission

    story = []

    story.append(

    Paragraph(

        "<font color='#2563EB'><b>DriveShare</b></font>",

        styles["Title"],

    )

)

    story.append(
        Paragraph(
            "Payment Receipt",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    data = [

    ["Invoice No", invoice_number],

    ["Generated On", generated_date],

    ["Receipt No", payment.id],

    [
        "Customer",
        payment.customer.get_full_name()
        or payment.customer.username,
    ],

    [
        "Owner",
        payment.booking.car.owner.get_full_name()
        or payment.booking.car.owner.username,
    ],

    [
        "Car",
        payment.booking.car.title,
    ],

    [
        "Booking Dates",
        f"{payment.booking.start_date} → {payment.booking.end_date}",
    ],

    [
        "Transaction ID",
        payment.transaction_id or "-",
    ],

    [
        "Payment Method",
        payment.payment_method or "-",
    ],

    [
        "Amount Paid",
        f"₹{payment.amount}",
    ],

    [
        "Platform Commission",
        f"₹{commission}",
    ],

    [
        "Owner Earnings",
        f"₹{owner_amount}",
    ],

    [
        "Status",
        payment.payment_status,
    ],

]
    table = Table(
    data,
    colWidths=[2.2 * inch, 4 * inch]
)

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

                ("TOPPADDING", (0, 0), (-1, -1), 10),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ]

        )

    )

    story.append(table)

    story.append(Spacer(1, 0.4 * inch))
    story.append(

    Paragraph(

        "<b>Thank you for choosing DriveShare.</b>",

        styles["Heading3"],

    )

)

    story.append(

    Paragraph(

        "This is a computer-generated receipt and does not require a signature.",

        styles["Normal"],

    )

)

    doc.build(story)

    return response



@login_required
@customer_required
def wallet(request):

    wallet = get_object_or_404(
        Wallet,
        customer=request.user
    )

    transactions = wallet.transactions.all().order_by(
        "-created_at"
    )

    paginator = Paginator(
        transactions,
        10
    )

    page = request.GET.get("page")

    transactions = paginator.get_page(page)
    

    return render(
        request,
        "bookings/wallet.html",
        {
            "wallet": wallet,
            "transactions": transactions,
        }
    )

from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from bookings.models import Payment





from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Payment, Booking


@login_required
def owner_earnings(request):

    if request.user.user_type != "owner":
        return redirect("home")

    COMMISSION_PERCENT = Decimal("10")

    payments = Payment.objects.filter(
        booking__car__owner=request.user,
        payment_status="Paid",
    ).select_related(
        "booking",
        "booking__car",
        "booking__customer",
    )

    gross_earnings = (
        payments.aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    commission = (
        gross_earnings * COMMISSION_PERCENT
    ) / Decimal("100")

    withdrawable = (
        gross_earnings - commission
    )

    completed_rentals = Booking.objects.filter(
        car__owner=request.user,
        booking_status="Completed"
    ).count()

    recent_transactions = payments.order_by(
        "-paid_at"
    )

    monthly_earnings = (
        payments
        .annotate(
            month=TruncMonth("paid_at")
        )
        .values("month")
        .annotate(
            total=Sum("owner_amount")
        )
        .order_by("month")
    )

    chart_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_earnings
        if item["month"]
    ]

    chart_values = [
        float(item["total"] or 0)
        for item in monthly_earnings
    ]

    context = {
        "payments": payments,

        "gross_earnings": gross_earnings,

        "commission": commission,

        "withdrawable": withdrawable,

        "completed_rentals": completed_rentals,

        "recent_transactions": recent_transactions,

        "chart_labels": json.dumps(chart_labels),

        "chart_values": json.dumps(chart_values),
    }

    return render(
        request,
        "bookings/owner_earnings.html",
        context,
    )
from django.db.models.functions import TruncMonth
from django.db.models import Sum
@login_required
@customer_required
def submit_payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    if booking.booking_status != "Approved":

        messages.error(
            request,
            "Payment is available only for approved bookings."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    payment = get_object_or_404(
        Payment,
        booking=booking,
        customer=request.user
    )

    if payment.payment_status == "Paid":

        messages.info(
            request,
            "This booking has already been paid."
        )

        return redirect(
            "booking_details",
            booking.id
        )

    if request.method != "POST":

        return redirect(
            "payment_page",
            booking.id
        )

    transaction_id = request.POST.get(
        "transaction_id",
        ""
    ).strip()

    screenshot = request.FILES.get(
        "payment_screenshot"
    )

    if not transaction_id:

        messages.error(
            request,
            "Please enter the UTR / transaction ID."
        )

        return redirect(
            "payment_page",
            booking.id
        )

    if not screenshot:

        messages.error(
            request,
            "Please upload your payment screenshot."
        )

        return redirect(
            "payment_page",
            booking.id
        )

    payment.transaction_id = transaction_id
    payment.payment_method = "UPI"
    payment.payment_screenshot = screenshot

    # IMPORTANT
    # Still waiting for owner verification.
    payment.payment_status = "Pending"

    payment.save()

    create_notification(
        user=booking.customer,
        title="Payment Proof Submitted",
        message=(
            f"Payment proof for "
            f"{booking.car.title} has been submitted. "
            f"Waiting for owner verification."
        ),
        notification_type="Payment",
        redirect_url=(
            f"/bookings/details/{booking.id}/"
        ),
    )

    create_notification(
        user=booking.car.owner,
        title="Payment Verification Required",
        message=(
            f"{booking.customer.get_full_name()} "
            f"or {booking.customer.username} "
            f"submitted payment proof for "
            f"{booking.car.title}. "
            f"UTR: {transaction_id}"
        ),
        notification_type="Payment",
        redirect_url=(
            f"/bookings/owner/details/{booking.id}/"
        ),
    )

    messages.success(
        request,
        "Payment proof submitted. "
        "Waiting for owner verification."
    )

    return redirect(
        "booking_details",
        booking.id
    )

@login_required
@owner_required
def verify_payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__owner=request.user
    )

    payment = get_object_or_404(
        Payment,
        booking=booking
    )

    if payment.payment_status == "Paid":

        messages.info(
            request,
            "Payment has already been verified."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    if booking.booking_status != "Approved":

        messages.error(
            request,
            "Only approved bookings can have payments verified."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    if payment.payment_method != "UPI":

        messages.error(
            request,
            "This payment does not require manual UPI verification."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    if not payment.transaction_id:

        messages.error(
            request,
            "Transaction ID is missing."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    if not payment.payment_screenshot:

        messages.error(
            request,
            "Payment screenshot is missing."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    # ---------------------------------------------
    # VERIFY PAYMENT
    # ---------------------------------------------

    payment.payment_status = "Paid"
    payment.verified_at = timezone.now()
    payment.verified_by = request.user
    payment.paid_at = timezone.now()

    payment.commission = (
        payment.amount * Decimal("10")
    ) / Decimal("100")

    payment.owner_amount = (
        payment.amount
        - payment.commission
    )

    payment.save()

    # ---------------------------------------------
    # CUSTOMER NOTIFICATION
    # ---------------------------------------------

    create_notification(
        user=booking.customer,
        title="Payment Verified",
        message=(
            f"Your payment of ₹{payment.amount} "
            f"for {booking.car.title} "
            f"has been verified successfully."
        ),
        notification_type="Payment",
        redirect_url=(
            f"/bookings/details/{booking.id}/"
        ),
    )

    messages.success(
        request,
        "Payment verified successfully."
    )

    return redirect(
        "owner_booking_details",
        booking.id
    )
@login_required
@owner_required
def reject_payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__owner=request.user
    )

    payment = get_object_or_404(
        Payment,
        booking=booking
    )

    if payment.payment_status == "Paid":

        messages.error(
            request,
            "A paid payment cannot be rejected."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    if request.method != "POST":

        return redirect(
            "owner_booking_details",
            booking.id
        )

    payment.payment_status = "Failed"

    payment.save(
        update_fields=[
            "payment_status",
        ]
    )

    create_notification(
        user=booking.customer,
        title="Payment Proof Rejected",
        message=(
            f"Your payment proof for "
            f"{booking.car.title} was rejected. "
            f"Please check your UTR and screenshot "
            f"and submit the payment proof again."
        ),
        notification_type="Payment",
        redirect_url=(
            f"/bookings/details/{booking.id}/"
        ),
    )

    messages.warning(
        request,
        "Payment proof rejected."
    )

    return redirect(
        "owner_booking_details",
        booking.id
    )