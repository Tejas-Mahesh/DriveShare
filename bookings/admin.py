from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
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
from .models import Payment

admin.site.register(Payment)
from .models import Wallet
from .models import WalletTransaction

admin.site.register(Wallet)
admin.site.register(WalletTransaction)
