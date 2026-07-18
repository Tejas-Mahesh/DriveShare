from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from .models import Wallet


@receiver(post_save, sender=CustomUser)
def create_wallet(sender, instance, created, **kwargs):

    if created and instance.user_type == "customer":

        Wallet.objects.create(
            customer=instance
        )