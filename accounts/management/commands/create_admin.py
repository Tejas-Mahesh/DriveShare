import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the DriveShare admin user"

    def handle(self, *args, **options):

        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")
        email = os.getenv("ADMIN_EMAIL", "")

        # --------------------------------------------------
        # Check environment variables
        # --------------------------------------------------

        if not username:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_USERNAME is not set."
                )
            )
            return

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_PASSWORD is not set."
                )
            )
            return

        # --------------------------------------------------
        # Find or create admin
        # --------------------------------------------------

        user, created = User.objects.get_or_create(
            username=username
        )

        # --------------------------------------------------
        # Set admin properties
        # --------------------------------------------------

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        if email:
            user.email = email

        # Always set password from Render environment
        user.set_password(password)

        # Superuser gets admin privileges regardless
        # of the normal customer/owner user_type system.
        user.save()

        # --------------------------------------------------
        # Message
        # --------------------------------------------------

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' created successfully."
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' updated successfully."
                )
            )