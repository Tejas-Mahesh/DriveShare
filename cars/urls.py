from django.urls import path
from . import views

urlpatterns = [

    path(
        "add/",
        views.add_car,
        name="add_car"
    ),

    path(
        "my-cars/",
        views.my_cars,
        name="my_cars"
    ),
    path(
    "edit/<int:car_id>/",
    views.edit_car,
    name="edit_car"
),
path(
    "delete/<int:car_id>/",
    views.delete_car,
    name="delete_car"
),
path(
    "admin/pending/",
    views.admin_car_list,
    name="admin_car_list"
),
path(
    "admin/review/<int:car_id>/",
    views.admin_review_car,
    name="admin_review_car"
),
path(
    "admin/approve/<int:car_id>/",
    views.approve_car,
    name="approve_car"
),
path(
    "admin/reject/<int:car_id>/",
    views.reject_car,
    name="reject_car"
),
path(
    "browse/",
    views.browse_cars,
    name="browse_cars"
),
]