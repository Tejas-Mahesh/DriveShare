from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views


urlpatterns = [

    path("admin/", admin.site.urls),

    # Home
    path("", views.home, name="home"),

    # Contact
    path("contact/", views.contact, name="contact"),

    # Accounts
    path("accounts/", include("accounts.urls")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # Cars
    path("cars/", include("cars.urls")),

    # Notifications
    path("notifications/", include("notifications.urls")),

    # Bookings
    path("bookings/", include("bookings.urls")),
]


handler403 = "core.views.error_403"


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )