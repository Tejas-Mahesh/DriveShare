"""
Django settings for DriveShare project.
"""

from pathlib import Path
import os

from dotenv import load_dotenv
import cloudinary
import dj_database_url


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

# Local .env file.
# On Render, variables are supplied through Render Environment Variables.

load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. "
        "Please configure SECRET_KEY in your environment variables."
    )


# ============================================================
# DEBUG
# ============================================================

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    # --------------------------------------------------------
    # Django
    # --------------------------------------------------------

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --------------------------------------------------------
    # Third-party
    # --------------------------------------------------------

    "cloudinary",
    "cloudinary_storage",

    # --------------------------------------------------------
    # DriveShare apps
    # --------------------------------------------------------

    "core",
    "accounts",
    "cars",
    "bookings.apps.BookingsConfig",
    "dashboard",
    "notifications",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "DriveShare.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [

    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

                "notifications.context_processors.notification_count",

            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "DriveShare.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

# ------------------------------------------------------------
# LOCAL
# ------------------------------------------------------------
# If DATABASE_URL is not present, SQLite is used.
#
# ------------------------------------------------------------
# RENDER
# ------------------------------------------------------------
# If DATABASE_URL is provided by Render,
# PostgreSQL will automatically be used.
# ------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL:

    DATABASES = {

        "default": dj_database_url.parse(

            DATABASE_URL,

            conn_max_age=600,

            ssl_require=True,
        )
    }

else:

    DATABASES = {

        "default": {

            "ENGINE": "django.db.backends.sqlite3",

            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"


STATICFILES_DIRS = [
    BASE_DIR / "static",
]


STATIC_ROOT = BASE_DIR / "staticfiles"


# ------------------------------------------------------------
# WhiteNoise
# ------------------------------------------------------------

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# CLOUDINARY
# ============================================================

cloudinary.config(

    cloud_name=os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    ),

    api_key=os.getenv(
        "CLOUDINARY_API_KEY"
    ),

    api_secret=os.getenv(
        "CLOUDINARY_API_SECRET"
    ),
)


DEFAULT_FILE_STORAGE = (
    "cloudinary_storage.storage.MediaCloudinaryStorage"
)


# ============================================================
# CUSTOM USER MODEL
# ============================================================

AUTH_USER_MODEL = "accounts.CustomUser"


# ============================================================
# LOGIN / LOGOUT
# ============================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "home"


# ============================================================
# RAZORPAY
# ============================================================




# ============================================================
# HTTPS / RENDER PROXY
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)