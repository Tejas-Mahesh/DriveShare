from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notification_list(request):

    notifications = request.user.notifications.order_by("-created_at")

    # Mark all notifications as read
    notifications.update(is_read=True)
    notifications = request.user.notifications.order_by("-created_at")

    unread_count = notifications.filter(
    is_read=False
    ).count()
    notifications.filter(
    is_read=False
).update(
    is_read=True
)
    return render(
    request,
    "notifications/notification_list.html",
    {
        "notifications": notifications,
        "unread_count": unread_count,
    }
)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
@login_required
def mark_all_notifications_read(request):

    request.user.notifications.update(
        is_read=True
    )

    return redirect("notifications")


@login_required
def delete_notification(request, notification_id):

    notification = get_object_or_404(

        request.user.notifications,

        id=notification_id,

    )

    notification.delete()

    return redirect("notifications")


@login_required
def clear_notifications(request):

    request.user.notifications.all().delete()

    return redirect("notifications")