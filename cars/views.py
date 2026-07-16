from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CarForm, CarImageForm
from .models import Car,CarImage
from accounts.decorators import owner_required
from notifications.models import Notification
from django.core.paginator import Paginator
@login_required
@owner_required
def add_car(request):

    if request.method == "POST":

        form = CarForm(
    request.POST,
    request.FILES
)

        

        if form.is_valid():

            car = form.save(commit=False)

            car.owner = request.user

            car.save()

            images = request.FILES.getlist("images")

            for index, image in enumerate(images):
                CarImage.objects.create(

                     car=car,

                    image=image,

                    is_primary=(index == 0)

                    )

            messages.success(
    request,
    f"{car.brand} {car.model} has been submitted for admin approval."
)

            return redirect("owner_dashboard")

    else:

        form = CarForm()

        

    return render(
        request,
        "cars/add_car.html",
        {
            
          "form": form,
    

        }
    )
@login_required
@owner_required
def my_cars(request):

    cars = Car.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    return render(
        request,
        "cars/my_cars.html",
        {
            "cars": cars
        }
    )

from django.shortcuts import get_object_or_404


@login_required
@owner_required
def edit_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user
    )

    if car.approval_status == "Approved":

        messages.error(
            request,
            "Approved cars cannot be edited."
        )

        return redirect("my_cars")

    if request.method == "POST":

        form = CarForm(
            request.POST,
            request.FILES,
            instance=car
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Car details updated successfully."
            )

            return redirect("my_cars")

    else:

        form = CarForm(instance=car)

    return render(
        request,
        "cars/edit_car.html",
        {
            "form": form,
            "car": car
        }
    )
@login_required
@owner_required
def delete_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user
    )

    if car.approval_status == "Approved":

        messages.error(
            request,
            "Approved cars cannot be deleted."
        )

        return redirect("my_cars")

    if request.method == "POST":

        car.delete()

        messages.success(
            request,
            "Car deleted successfully."
        )

        return redirect("my_cars")

    return render(
        request,
        "cars/delete_car.html",
        {
            "car": car
        }
    )

from accounts.decorators import admin_required


@login_required
@admin_required
def admin_car_list(request):

    pending_cars = Car.objects.filter(
        approval_status="Pending"
    ).order_by("-created_at")

    return render(
        request,
        "cars/admin_car_list.html",
        {
            "pending_cars": pending_cars
        }
    )

@login_required
@admin_required
def admin_review_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id
    )

    return render(
        request,
        "cars/admin_review_car.html",
        {
            "car": car
        }
    )
@login_required
@admin_required
def approve_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id
    )

    car.approval_status = "Approved"

    car.save()
    Notification.objects.create(
    user=car.owner,
    title="Car Approved",
    message=f"Your car '{car.title}' has been approved and is now visible to customers."
)

    messages.success(
        request,
        f"{car.brand} {car.model} has been approved."
    )

    return redirect("admin_car_list")

@login_required
@admin_required
def reject_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id
    )

    if request.method == "POST":

        reason = request.POST.get("reason")

        car.approval_status = "Rejected"
        car.rejection_reason = reason

        car.save()
        Notification.objects.create(
    user=car.owner,
    title="Car Rejected",
    message=f"Your car '{car.title}' was rejected.\n\nReason:\n{reason}"
)

        messages.success(
            request,
            "Car rejected successfully."
        )

        return redirect("admin_car_list")

    return render(
        request,
        "cars/reject_car.html",
        {
            "car": car
        }
    )
from django.db.models import Q

def browse_cars(request):

    cars = Car.objects.filter(
        approval_status="Approved",
        is_available=True
    )

    search = request.GET.get("search")
    fuel = request.GET.get("fuel")
    transmission = request.GET.get("transmission")
    seats = request.GET.get("seats")
    city = request.GET.get("city")

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    if search:
        cars = cars.filter(
            Q(title__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search) |
            Q(city__icontains=search)
        )

    if fuel:
        cars = cars.filter(fuel_type=fuel)

    if transmission:
        cars = cars.filter(transmission=transmission)

    if seats:
        cars = cars.filter(seats=seats)

    if city:
        cars = cars.filter(city__icontains=city)

    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)

    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)

    if sort == "low":
        cars = cars.order_by("price_per_day")

    elif sort == "high":
        cars = cars.order_by("-price_per_day")

    elif sort == "old":
        cars = cars.order_by("created_at")

    else:
        cars = cars.order_by("-created_at")

    return render(
        request,
        "cars/browse_cars.html",
        {
            "cars": cars,
            "search": search,
            "fuel": fuel,
            "transmission": transmission,
            "seats": seats,
            "city": city,
            "min_price": min_price,
            "max_price": max_price,
            "sort": sort,
        }
    )
from django.shortcuts import get_object_or_404


def car_details(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        approval_status="Approved"
    )

    return render(
        request,
        "cars/car_details.html",
        {
            "car": car
        }
    )