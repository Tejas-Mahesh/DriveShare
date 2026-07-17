from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "car",
        "start_date",
        "end_date",
        "booking_status",
    )

    list_filter = (
        "booking_status",
        "start_date",
    )

    search_fields = (
        "customer__username",
        "car__title",
    )