from django.urls import path
from . import views

urlpatterns = [

    path("", views.notification_list, name="notifications"),

    path(
        "read-all/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),

    path(
        "delete/<int:notification_id>/",
        views.delete_notification,
        name="delete_notification",
    ),

    path(
        "clear/",
        views.clear_notifications,
        name="clear_notifications",
    ),

]