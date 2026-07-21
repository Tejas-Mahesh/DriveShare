from django.urls import path

from . import views

urlpatterns = [

    path(
        "customer/",
        views.customer_dashboard,
        name="customer_dashboard"
    ),

    path(
        "owner/",
        views.owner_dashboard,
        name="owner_dashboard"
    ),
    path(
        "admin/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),
    path("about/", views.about, name="about"),

path("contact/", views.contact, name="contact"),
path(
    "dashboard/revenue/",
    views.revenue_report,
    name="revenue_report",
),

]
