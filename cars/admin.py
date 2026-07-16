from django.contrib import admin
from .models import Car, CarImage

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "brand",
        "model",
        "owner",
        "city",
        "price_per_day",
        "approval_status",
        "is_available",
        "created_at",
    )

    list_filter = (
        "approval_status",
        "fuel_type",
        "transmission",
        "city",
        "is_available",
    )

    search_fields = (
        "title",
        "brand",
        "model",
        "owner__username",
        "city",
    )

    list_editable = (
        "approval_status",
        "is_available",
    )

    ordering = ("-created_at",)

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "car",
        "is_primary",
        "uploaded_at",
    )

    list_filter = (
        "is_primary",
    )