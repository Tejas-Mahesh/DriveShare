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
echo "Creating production admin user..."
echo "=========================================="

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")

if not username or not email or not password:
    raise RuntimeError(
        "ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD "
        "must be configured in Render Environment Variables."
    )

user = User.objects.filter(username=username).first()

if user:
    print(f"Admin user '{username}' already exists.")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )

    print(f"Admin user '{username}' created successfully.")

print("Production admin setup completed.")
PY


echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="