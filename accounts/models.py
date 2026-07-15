from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    USER_TYPES = (

        ('customer', 'Customer'),

        ('owner', 'Car Owner'),

        ('admin', 'Admin'),

    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='customer'
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):

        return self.username
    

class CustomerProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    address = models.TextField(blank=True)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    aadhaar_number = models.CharField(
        max_length=12,
        blank=True
    )

    aadhaar_photo = models.ImageField(
        upload_to="customer/aadhaar/",
        blank=True,
        null=True
    )

    driving_license_number = models.CharField(
        max_length=25,
        blank=True
    )

    driving_license_photo = models.ImageField(
        upload_to="customer/license/",
        blank=True,
        null=True
    )

    emergency_contact = models.CharField(
        max_length=15,
        blank=True
    )
    verification_status = models.CharField(
    max_length=20,
    choices=[
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ],
    default="Pending"
    )

    profile_completed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username
    
class OwnerProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="owner_profile"
    )

    address = models.TextField(blank=True)

    aadhaar_number = models.CharField(
        max_length=12,
        blank=True
    )

    aadhaar_photo = models.ImageField(
        upload_to="owner/aadhaar/",
        blank=True,
        null=True
    )

    driving_license_number = models.CharField(
        max_length=25,
        blank=True
    )

    driving_license_photo = models.ImageField(
        upload_to="owner/license/",
        blank=True,
        null=True
    )

    pan_number = models.CharField(
        max_length=10,
        blank=True
    )

    bank_account = models.CharField(
        max_length=30,
        blank=True
    )

    ifsc_code = models.CharField(
        max_length=15,
        blank=True
    )

    verification_status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected"),
        ],
        default="Pending"
    )

    profile_completed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username