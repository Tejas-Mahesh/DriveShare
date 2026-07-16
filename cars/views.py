from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CarForm, CarImageForm
from .models import Car,CarImage
from accounts.decorators import owner_required
from notifications.models import Notification

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
def browse_cars(request):

    cars = Car.objects.filter(
        approval_status="Approved",
        is_available=True
    ).order_by("-created_at")

    return render(
        request,
        "cars/browse_cars.html",
        {
            "cars": cars
        }
    )