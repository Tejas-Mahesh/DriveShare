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

]