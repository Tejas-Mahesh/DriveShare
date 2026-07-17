from django.db import models
from accounts.models import CustomUser


class Car(models.Model):

    FUEL_TYPES = [

        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Electric", "Electric"),
        ("Hybrid", "Hybrid"),
        ("CNG", "CNG"),
    ]

    TRANSMISSION_TYPES = [

        ("Manual", "Manual"),
        ("Automatic", "Automatic"),
    ]

    STATUS_CHOICES = [

        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cars"
    )

    title = models.CharField(max_length=150)

    brand = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    year = models.PositiveIntegerField()

    color = models.CharField(max_length=50)

    seats = models.PositiveIntegerField()

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPES
    )

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_TYPES
    )

    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    city = models.CharField(max_length=100)

    description = models.TextField()

    is_available = models.BooleanField(default=True)

    approval_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    rejection_reason = models.TextField(
    blank=True,
    null=True
)
    

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return f"{self.brand} {self.model} ({self.year}) - {self.owner.username}"
    
class CarImage(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="car_images/"
    )

    is_primary = models.BooleanField(
        default=False
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.car.title} Image"

class Wishlist(models.Model):

    customer = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("customer", "car")

    def __str__(self):
        return f"{self.customer.username} - {self.car.title}"