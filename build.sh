#!/usr/bin/env bash

set -o errexit

echo "=========================================="
echo "Installing dependencies..."
echo "=========================================="

pip install -r requirements.txt


echo "=========================================="
echo "Collecting static files..."
echo "=========================================="

python manage.py collectstatic --no-input


echo "=========================================="
echo "Running database migrations..."
echo "=========================================="

python manage.py migrate


echo "=========================================="
echo "Setting up production admin..."
echo "=========================================="

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")

if not username:
    raise RuntimeError("ADMIN_USERNAME is not configured.")

if not email:
    raise RuntimeError("ADMIN_EMAIL is not configured.")

if not password:
    raise RuntimeError("ADMIN_PASSWORD is not configured.")


# Find existing user or create a new one
user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email,
    }
)


# Update email
user.email = email


# IMPORTANT:
# Make the account a Django administrator
user.is_staff = True
user.is_superuser = True
user.is_active = True


# Set password
user.set_password(password)

user.save()


if created:
    print(f"Admin user '{username}' CREATED successfully.")
else:
    print(f"Existing user '{username}' UPDATED to SUPERUSER.")


print("==========================================")
print(f"Username: {username}")
print(f"Is staff: {user.is_staff}")
print(f"Is superuser: {user.is_superuser}")
print(f"Is active: {user.is_active}")
print("Production admin setup completed.")
print("==========================================")
PY


echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="