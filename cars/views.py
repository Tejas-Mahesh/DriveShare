from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.db.models import (
    Q,
    Avg,
    Count,
    Prefetch,
)

from django.db.models.functions import Length

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.http import HttpResponse

from .forms import CarForm

from .models import (
    Car,
    CarImage,
    Wishlist,
)

from accounts.decorators import (
    owner_required,
    customer_required,
    admin_required,
)

from notifications.models import Notification
from bookings.models import Booking


# ============================================================
# ADD CAR
# ============================================================

@login_required
@owner_required
def add_car(request):

    if request.method == "POST":

        form = CarForm(request.POST, request.FILES)

        if form.is_valid():

            car = form.save(commit=False)
            car.owner = request.user
            car.approval_status = "Pending"
            car.is_available = True
            car.save()

            # Save uploaded images directly into database
            images = request.FILES.getlist("images")

            for index, image in enumerate(images):

                CarImage.objects.create(
                    car=car,
                    image_data=image.read(),
                    image_name=image.name,
                    image_type=image.content_type or "image/jpeg",
                    is_primary=(index == 0),
                )

            messages.success(
                request,
                f"{car.brand} {car.model} has been submitted for admin approval."
            )

            return redirect("owner_dashboard")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = CarForm()

    return render(
        request,
        "cars/add_car.html",
        {"form": form}
    )

# ============================================================
# MY CARS
# ============================================================

@login_required
@owner_required
def my_cars(request):

    cars = (
        Car.objects
        .filter(owner=request.user)
        .order_by("-created_at")
    )

    for car in cars:

        car.has_booking = (
            Booking.objects
            .filter(car=car)
            .exists()
        )

        car.can_delete = not car.has_booking

    return render(
        request,
        "cars/my_cars.html",
        {
            "cars": cars,
        }
    )


# ============================================================
# EDIT CAR
# ============================================================

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

        return redirect(
            "my_cars"
        )

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

            return redirect(
                "my_cars"
            )

    else:

        form = CarForm(
            instance=car
        )

    return render(
        request,
        "cars/edit_car.html",
        {
            "form": form,
            "car": car,
        }
    )


# ============================================================
# ADMIN CAR LIST
# ============================================================

@login_required
@admin_required
def admin_car_list(request):

    pending_cars = (
        Car.objects
        .filter(
            approval_status="Pending"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "cars/admin_car_list.html",
        {
            "pending_cars": pending_cars,
        }
    )


# ============================================================
# ADMIN REVIEW
# ============================================================

# ============================================================
# ADMIN REVIEW
# ============================================================

@login_required
@admin_required
def admin_review_car(request, car_id):

    valid_images = (
        CarImage.objects
        .annotate(
            data_length=Length("image_data")
        )
        .filter(
            image_data__isnull=False,
            data_length__gt=0
        )
        .order_by(
            "-is_primary",
            "id"
        )
    )

    car = get_object_or_404(
        Car,
        id=car_id
    )

    # Attach only images that actually contain data
    car.valid_images = list(
        valid_images.filter(car=car)
    )

    return render(
        request,
        "cars/admin_review_car.html",
        {
            "car": car,
        }
    )


# ============================================================
# APPROVE CAR
# ============================================================

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

        message=(
            f"Your car '{car.title}' has been "
            "approved and is now visible to customers."
        )
    )

    messages.success(
        request,
        f"{car.brand} {car.model} has been approved."
    )

    return redirect(
        "admin_car_list"
    )


# ============================================================
# REJECT CAR
# ============================================================

@login_required
@admin_required
def reject_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id
    )

    if request.method == "POST":

        reason = request.POST.get(
            "reason",
            ""
        )

        car.approval_status = "Rejected"

        car.rejection_reason = reason

        car.save()

        Notification.objects.create(

            user=car.owner,

            title="Car Rejected",

            message=(
                f"Your car '{car.title}' "
                "was rejected.\n\n"
                f"Reason:\n{reason}"
            )
        )

        messages.success(
            request,
            "Car rejected successfully."
        )

        return redirect(
            "admin_car_list"
        )

    return render(
        request,
        "cars/reject_car.html",
        {
            "car": car,
        }
    )


# ============================================================
# BROWSE CARS
# ============================================================



from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q, Prefetch
from django.db.models.functions import Length
from django.shortcuts import render

from .models import Car, CarImage


def browse_cars(request):
    search = request.GET.get("search", "")
    fuel = request.GET.get("fuel", "")
    transmission = request.GET.get("transmission", "")
    seats = request.GET.get("seats", "")
    city = request.GET.get("city", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    sort = request.GET.get("sort", "")

    # =========================================================
    # VALID CAR IMAGES
    # =========================================================
    valid_images = (
        CarImage.objects
        .filter(image_data__isnull=False)
        .annotate(data_length=Length("image_data"))
        .filter(data_length__gt=0)
        .exclude(image_name="")
        .order_by("-is_primary", "id")
    )

    # =========================================================
    # CARS
    # =========================================================
    cars = (
        Car.objects
        .filter(
            approval_status="Approved",
            is_available=True
        )
        .select_related("owner")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=valid_images,
                to_attr="valid_images"
            )
        )
        .annotate(
            average_rating=Avg("reviews__rating"),
            total_reviews=Count("reviews")
        )
    )

    # =========================================================
    # SEARCH
    # =========================================================
    if search:
        cars = cars.filter(
            Q(brand__icontains=search) |
            Q(model__icontains=search) |
            Q(city__icontains=search)
        )

    # =========================================================
    # FILTERS
    # =========================================================
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

    # =========================================================
    # SORTING
    # =========================================================
    if sort == "low":
        cars = cars.order_by("price_per_day")

    elif sort == "high":
        cars = cars.order_by("-price_per_day")

    elif sort == "old":
        cars = cars.order_by("created_at")

    else:
        cars = cars.order_by("-created_at")

    # =========================================================
    # WISHLIST
    # =========================================================
    wishlist_ids = []

    if request.user.is_authenticated:
        wishlist_ids = list(
            request.user.wishlist_items.values_list(
                "car_id",
                flat=True
            )
        )

    # =========================================================
    # PAGINATION
    # =========================================================
    paginator = Paginator(cars, 9)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    cars_page = page_obj.object_list

    # =========================================================
    # CONTEXT
    # =========================================================
    context = {
        "cars": cars_page,
        "page_obj": page_obj,

        "search": search,
        "fuel": fuel,
        "transmission": transmission,
        "seats": seats,
        "city": city,

        "min_price": min_price,
        "max_price": max_price,

        "sort": sort,

        "wishlist_ids": wishlist_ids,
    }

    return render(
        request,
        "cars/browse_cars.html",
        context
    )
# ============================================================
# CAR DETAILS
# ============================================================
# ============================================================
# CAR DETAILS
# ============================================================

def car_details(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        approval_status="Approved"
    )

    # =========================================================
    # VALID IMAGES FOR CURRENT CAR
    # =========================================================

    valid_images = (
        CarImage.objects
        .filter(
            car=car,
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

    # Convert to list so template can safely use it
    car.valid_images = list(valid_images)

    # =========================================================
    # SIMILAR CARS
    # =========================================================

    similar_cars = list(
        Car.objects
        .filter(
            approval_status="Approved",
            is_available=True,
            brand=car.brand
        )
        .exclude(
            id=car.id
        )
        .prefetch_related(
            Prefetch(
                "images",
                queryset=(
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
                ),
                to_attr="valid_images"
            )
        )[:4]
    )

    # =========================================================
    # IF LESS THAN 4 SIMILAR CARS
    # =========================================================

    if len(similar_cars) < 4:

        additional = list(
            Car.objects
            .filter(
                approval_status="Approved",
                is_available=True,
                fuel_type=car.fuel_type
            )
            .exclude(
                id__in=[
                    c.id for c in similar_cars
                ] + [car.id]
            )
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=(
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
                    ),
                    to_attr="valid_images"
                )
            )[
                :4 - len(similar_cars)
            ]
        )

        similar_cars.extend(additional)

    # =========================================================
    # OWNER
    # =========================================================

    owner = car.owner

    owner_total_cars = (
        Car.objects
        .filter(
            owner=owner,
            approval_status="Approved"
        )
        .count()
    )

    # =========================================================
    # REVIEWS
    # =========================================================

    reviews = (
        car.reviews
        .select_related("customer")
        .order_by("-created_at")
    )

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    review_count = reviews.count()

    # =========================================================
    # CONTEXT
    # =========================================================

    return render(
        request,
        "cars/car_details.html",
        {
            "car": car,
            "similar_cars": similar_cars,
            "owner": owner,
            "owner_total_cars": owner_total_cars,
            "reviews": reviews,
            "average_rating": average_rating,
            "review_count": review_count,
        }
    )

# ============================================================
# TOGGLE WISHLIST
# ============================================================

@login_required
@customer_required
def toggle_wishlist(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        approval_status="Approved"
    )

    wishlist_item = (
        Wishlist.objects
        .filter(
            customer=request.user,
            car=car
        )
        .first()
    )

    if wishlist_item:

        wishlist_item.delete()

        messages.success(
            request,
            "Car removed from your wishlist."
        )

    else:

        Wishlist.objects.create(

            customer=request.user,

            car=car
        )

        messages.success(
            request,
            "Car added to your wishlist."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "browse_cars"
        )
    )


# ============================================================
# WISHLIST
# ============================================================

@login_required
@customer_required
def wishlist(request):

    wishlist_items = (

        Wishlist.objects

        .filter(
            customer=request.user
        )

        .select_related("car")

        .prefetch_related(
            "car__images"
        )

    )

    return render(
        request,
        "cars/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


# ============================================================
# DELETE CAR
# ============================================================

@login_required
@owner_required
def delete_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user
    )

    has_booking = (
        Booking.objects
        .filter(car=car)
        .exists()
    )

    if has_booking:

        messages.error(
            request,
            (
                "This car cannot be deleted "
                "because booking records exist."
            )
        )

        return redirect(
            "my_cars"
        )

    if request.method == "POST":

        car.delete()

        messages.success(
            request,
            "Car deleted successfully."
        )

        return redirect(
            "my_cars"
        )

    return render(
        request,
        "cars/delete_car.html",
        {
            "car": car
        }
    )


# ============================================================
# SERVE CAR IMAGE FROM DATABASE
# ============================================================



def car_image(request, image_id):

    image = get_object_or_404(
        CarImage,
        id=image_id
    )

    if not image.image_data:
        return HttpResponse(
            status=404
        )

    response = HttpResponse(
        image.image_data,
        content_type=image.image_type or "image/jpeg"
    )

    response["Cache-Control"] = "public, max-age=86400"

    return response