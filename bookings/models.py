from django.db import models
from accounts.models import CustomUser
from cars.models import Car


class Booking(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="customer_bookings"
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    start_date = models.DateField()

    end_date = models.DateField()

    total_days = models.PositiveIntegerField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    

    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    customer_message = models.TextField(
        blank=True
    )

    owner_message = models.TextField(
        blank=True
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    approved_at = models.DateTimeField(
    null=True,
    blank=True
)

    completed_at = models.DateTimeField(
    null=True,
    blank=True
)

    def __str__(self):
        return f"{self.customer.username} - {self.car.title}"

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
    

class Payment(models.Model):

    PAYMENT_STATUS = (

        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),

    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    payment_method = models.CharField(
        max_length=50,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.booking.id} - {self.payment_status}"
    
class Wallet(models.Model):

    customer = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.customer.username} Wallet"
class WalletTransaction(models.Model):

    TRANSACTION_TYPES = (

        ("Credit", "Credit"),

        ("Debit", "Debit"),

    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    description = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.wallet.customer.username} - {self.transaction_type}"