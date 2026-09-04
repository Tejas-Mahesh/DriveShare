from django.urls import path
from . import views


urlpatterns = [

    # =========================================================
    # OWNER - CAR MANAGEMENT
    # =========================================================

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


    # =========================================================
    # ADMIN - CAR MANAGEMENT
    # =========================================================

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


    # =========================================================
    # CUSTOMER - BROWSE
    # =========================================================

    path(
        "browse/",
        views.browse_cars,
        name="browse_cars"
    ),

    path(
        "details/<int:car_id>/",
        views.car_details,
        name="car_details"
    ),


    # =========================================================
    # WISHLIST
    # =========================================================

    path(
        "wishlist/<int:car_id>/",
        views.toggle_wishlist,
        name="toggle_wishlist"
    ),

    path(
        "wishlist/",
        views.wishlist,
        name="wishlist"
    ),


    # =========================================================
    # CAR IMAGE
    # =========================================================

    path(
        "image/<int:image_id>/",
        views.car_image,
        name="car_image"
    ),
]