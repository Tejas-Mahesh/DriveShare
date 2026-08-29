from django.contrib import admin

from .models import (
    Booking,
    Review,
    Payment,
    Wallet,
    WalletTransaction,
)


# =========================================================
# BOOKING
# =========================================================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "invoice_number",
        "customer",
        "car",
        "start_date",
        "end_date",
        "total_days",
        "total_amount",
        "booking_status",
        "booked_at",
    )

    list_filter = (
        "booking_status",
        "start_date",
        "end_date",
    )

    search_fields = (
        "invoice_number",
        "customer__username",
        "car__title",
        "car__owner__username",
    )

    ordering = (
        "-booked_at",
    )


# =========================================================
# REVIEW
# =========================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "booking",
        "customer",
        "car",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
    )

    search_fields = (
        "customer__username",
        "car__title",
        "review",
    )

    ordering = (
        "-created_at",
    )


# =========================================================
# PAYMENT
# =========================================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "booking",
        "customer",
        "amount",
        "payment_status",
        "payment_method",
        "transaction_id",
        "commission",
        "owner_amount",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "payment_method",
        "paid_at",
    )

    search_fields = (
        "transaction_id",
        "customer__username",
        "booking__invoice_number",
        "booking__car__title",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "commission",
        "owner_amount",
        "created_at",
    )


# =========================================================
# WALLET
# =========================================================

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "balance",
        "updated_at",
    )

    search_fields = (
        "customer__username",
    )

    ordering = (
        "-updated_at",
    )


# =========================================================
# WALLET TRANSACTION
# =========================================================

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "wallet",
        "amount",
        "transaction_type",
        "description",
        "created_at",
    )

    list_filter = (
        "transaction_type",
    )

    search_fields = (
        "wallet__customer__username",
        "description",
    )

    ordering = (
        "-created_at",
    )