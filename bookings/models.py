from django.db import models
from accounts.models import CustomUser
from cars.models import Car

from django.utils import timezone
from django.db import models
from decimal import Decimal



from django.db import models
from django.conf import settings
from django.utils import timezone


class Booking(models.Model):

    BOOKING_STATUS = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    car = models.ForeignKey(
        "cars.Car",
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    total_days = models.PositiveIntegerField(
        default=1
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    customer_message = models.TextField(
        blank=True,
        null=True
    )

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default="Pending"
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Booking #{self.id}"

    def save(self, *args, **kwargs):

        if not self.invoice_number:
            # Temporary invoice generation
            # after object gets an ID, you can improve this if needed
            pass

        super().save(*args, **kwargs)

        if not self.invoice_number:
            self.invoice_number = f"DS-{self.id:06d}"
            super().save(
                update_fields=["invoice_number"]
            )


class Payment(models.Model):

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]

    PAYMENT_METHOD = [
        ("UPI", "UPI"),
        ("Wallet", "Wallet"),
        ("Wallet + Razorpay", "Wallet + Razorpay"),
        ("Razorpay", "Razorpay"),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD,
        blank=True,
        null=True
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    payment_screenshot = models.ImageField(
        upload_to="payment_screenshots/",
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    verified_at = models.DateTimeField(
        blank=True,
        null=True
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="verified_payments"
    )

    commission = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    owner_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment #{self.id}"


class Wallet(models.Model):

    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.customer.username} - "
            f"₹{self.balance}"
        )


class WalletTransaction(models.Model):

    TRANSACTION_TYPES = [
        ("Credit", "Credit"),
        ("Debit", "Debit"),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    description = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.transaction_type} "
            f"₹{self.amount}"
        )

from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="review"
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    review = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.car.title} - {self.rating}★"
    

