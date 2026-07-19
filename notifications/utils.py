from .models import Notification


def create_notification(
    user,
    title,
    message,
    notification_type="System",
    redirect_url="",
):

    Notification.objects.create(

        user=user,

        title=title,

        message=message,

        notification_type=notification_type,

        redirect_url=redirect_url,

    )