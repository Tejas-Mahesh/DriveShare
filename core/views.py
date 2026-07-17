from django.shortcuts import render
from django.db.models import Avg, Count
from cars.models import Car
from bookings.models import Review
def error_403(request, exception):

    return render(
        request,
        "errors/403.html",
        status=403
    )
from cars.models import Car


def home(request):

    top_rated_cars = (
        Car.objects.filter(
            approval_status="Approved",
            is_available=True
        )
        .annotate(
            average_rating=Avg("reviews__rating"),
            review_count=Count("reviews")
        )
        .order_by("-average_rating", "-review_count")[:6]
    )
    recent_reviews = (
    Review.objects.select_related(
        "customer",
        "car"
    )
    .order_by("-created_at")[:6]
)

    return render(
    request,
    "home.html",
    {
        "top_rated_cars": top_rated_cars,
        "recent_reviews": recent_reviews,
    }
)