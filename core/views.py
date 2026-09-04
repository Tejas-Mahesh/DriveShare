from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Count, Prefetch
from django.db.models.functions import Length

from cars.models import Car, CarImage
from bookings.models import Review


# =========================================================
# 403 ERROR
# =========================================================

def error_403(request, exception):

    return render(
        request,
        "errors/403.html",
        status=403
    )


# =========================================================
# HOME PAGE
# =========================================================

def home(request):

    # -----------------------------------------------------
    # ONLY USE CAR IMAGES THAT ACTUALLY CONTAIN DATA
    # -----------------------------------------------------
    valid_images = (
        CarImage.objects
        .filter(
            image_data__isnull=False
        )
        .annotate(
            data_length=Length("image_data")
        )
        .filter(
            data_length__gt=0
        )
        .exclude(
            image_name=""
        )
        .order_by(
            "-is_primary",
            "id"
        )
    )


    # -----------------------------------------------------
    # TOP RATED CARS
    # -----------------------------------------------------
    top_rated_cars = (
        Car.objects
        .filter(
            approval_status="Approved",
            is_available=True
        )
        .prefetch_related(
            Prefetch(
                "images",
                queryset=valid_images,
                to_attr="valid_images"
            )
        )
        .annotate(
            average_rating=Avg("reviews__rating"),
            review_count=Count("reviews")
        )
        .order_by(
            "-average_rating",
            "-review_count"
        )[:6]
    )


    # -----------------------------------------------------
    # RECENT REVIEWS
    # -----------------------------------------------------
    recent_reviews = (
        Review.objects
        .select_related(
            "customer",
            "car"
        )
        .order_by(
            "-created_at"
        )[:6]
    )


    # -----------------------------------------------------
    # RENDER HOME PAGE
    # -----------------------------------------------------
    return render(
        request,
        "home.html",
        {
            "top_rated_cars": top_rated_cars,
            "recent_reviews": recent_reviews,
        }
    )

# =========================================================
# CONTACT PAGE
# =========================================================

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not subject:
            subject = "New Contact Message - DriveShare"

        email_message = f"""
You have received a new message from the DriveShare Contact Form.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

        try:

            send_mail(
                subject=f"DriveShare Contact: {subject}",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                fail_silently=False,
            )

            messages.success(
                request,
                "Your message has been sent successfully. We will contact you soon."
            )

        except Exception as e:

            print("CONTACT EMAIL ERROR:", e)

            messages.error(
                request,
                "Sorry, your message could not be sent. Please try again later."
            )

        return redirect("contact")

    return render(request, "contact.html")