from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    CustomUser,
    CustomerProfile,
    OwnerProfile
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "phone_number",
        "user_type",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (

        (
            "DriveShare Information",

            {
                "fields": (
                    "phone_number",
                    "user_type",
                    "profile_picture",
                )
            },

        ),

    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
    "user",
    "verification_status",
    "profile_completed",
    )
    search_fields = (
        "user__username",
        "aadhaar_number",
    )
    list_filter = (
    "verification_status",
    )


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "verification_status",
        "profile_completed",
    )

    search_fields = (
        "user__username",
        "pan_number",
    )

    list_filter = (
        "verification_status",
    )