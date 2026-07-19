from django.db import models
from django.conf import settings


class Notification(models.Model):

    NOTIFICATION_TYPES = (

    ("Booking", "Booking"),

    ("Payment", "Payment"),

    ("Wallet", "Wallet"),

    ("Coupon", "Coupon"),

    ("System", "System"),

)



    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        default="System",
    )

    is_read = models.BooleanField(
        default=False,
    )

    redirect_url = models.CharField(
        max_length=300,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.user.username} - {self.title}"