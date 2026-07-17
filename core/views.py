from django.shortcuts import render

from cars.models import Car

def error_403(request, exception):

    return render(
        request,
        "errors/403.html",
        status=403
    )
from cars.models import Car


def home(request):

    featured_cars = Car.objects.filter(
        approval_status="Approved",
        is_available=True
    ).order_by("-created_at")[:6]

    return render(
        request,
        "home.html",
        {
            "featured_cars": featured_cars,
        }
    )