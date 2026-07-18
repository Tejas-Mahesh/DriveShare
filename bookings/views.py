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

@login_required
@customer_required
def book_car(request, car_id):

    car = get_object_or_404(
        Car,
        id=car_id,
        approval_status="Approved",
        is_available=True,
    )

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.customer = request.user
            booking.car = car

            start = booking.start_date
            end = booking.end_date

            if start < date.today():

                messages.error(
                    request,
                    "Start date cannot be in the past."
                )

                return render(
                    request,
                    "bookings/book_car.html",
                    {
                        "form": form,
                        "car": car,
                    }
                )

            if end <= start:

                messages.error(
                    request,
                    "End date must be after the start date."
                )

                return render(
                    request,
                    "bookings/book_car.html",
                    {
                        "form": form,
                        "car": car,
                    }
                )
            existing_booking = Booking.objects.filter(
    car=car,
    booking_status="Approved"
).filter(
    Q(start_date__lte=end) &
    Q(end_date__gte=start)
).exists()

            if existing_booking:
                messages.error(
        request,
        "This car is already booked for the selected dates."
    )

                return render(
        request,
        "bookings/book_car.html",
        {
            "form": form,
            "car": car,
        }
    )

            booking.total_days = (end - start).days

            booking.total_amount = (
                booking.total_days * car.price_per_day
            )

            booking.save()

            messages.success(
                request,
                "Booking request submitted successfully."
            )

            return redirect("customer_dashboard")

    else:

        form = BookingForm()
    approved_bookings = Booking.objects.filter(
        car=car,
        booking_status="Approved"
    )


    return render(
    request,
    "bookings/book_car.html",
    {
        "form": form,
        "car": car,
        "approved_bookings": approved_bookings,
    }
)
from django.contrib.auth.decorators import login_required
from accounts.decorators import customer_required
from .models import Booking


from django.core.paginator import Paginator
from django.db.models import Q


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
@login_required
@customer_required
def booking_details(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    return render(
        request,
        "bookings/booking_details.html",
        {
            "booking": booking,
        }
    )
@login_required
@customer_required
def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    if booking.booking_status != "Pending":

        messages.error(
            request,
            "Only pending bookings can be cancelled."
        )

        return redirect("my_bookings")

    booking.booking_status = "Cancelled"

    booking.save()

    messages.success(
        request,
        "Your booking has been cancelled successfully."
    )

    return redirect("my_bookings")
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
        Booking,
        id=booking_id,
        car__owner=request.user
    )

    return render(
        request,
        "bookings/owner_booking_details.html",
        {
            "booking": booking,
        }
    )
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

        return redirect("owner_bookings")

    conflict = Booking.objects.filter(

        car=booking.car,

        booking_status="Approved",

       

        start_date__lte=booking.end_date,

        end_date__gte=booking.start_date,

    ).exclude(

        id=booking.id

    ).exists()

    if conflict:

        messages.error(
            request,
            "This car is already booked for the selected dates."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    booking.booking_status = "Approved"
    booking.approved_at = timezone.now()
    booking.save()

    

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

        return redirect("owner_bookings")

    booking.booking_status = "Rejected"

    booking.save()

    messages.success(
        request,
        "Booking rejected successfully."
    )

    return redirect("owner_booking_details", booking.id)
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
@owner_required
def complete_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__owner=request.user
    )

    if booking.booking_status == "Approved":

        booking.booking_status = "Completed"

        booking.save()

        messages.success(
            request,
            "Booking marked as completed."
        )

    return redirect(
        "owner_booking_details",
        booking.id
    )

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
        car__owner=request.user
    )

    if booking.booking_status != "Approved":

        messages.error(
            request,
            "Only approved bookings can be completed."
        )

        return redirect(
            "owner_booking_details",
            booking.id
        )

    booking.booking_status = "Completed"
    booking.completed_at = timezone.now()
    booking.save()

    messages.success(
        request,
        "Booking marked as completed successfully."
    )

    return redirect(
        "owner_booking_details",
        booking.id
    )