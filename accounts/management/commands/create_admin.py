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

        if not username:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_USERNAME is not set. Admin creation skipped."
                )
            )
            return

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    "ADMIN_PASSWORD is not set. Admin creation skipped."
                )
            )
            return

        admin, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "user_type": "customer",
            },
        )

        # Always make sure the account has admin privileges.
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True

        if email:
            admin.email = email

        # Set/update password from Render environment variable.
        admin.set_password(password)

        admin.save()

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