from django.urls import path
from . import views


urlpatterns = [

    # ==================================================
    # CUSTOMER
    # ==================================================

    path(
        "book/<int:car_id>/",
        views.book_car,
        name="book_car"
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "details/<int:booking_id>/",
        views.booking_details,
        name="booking_details"
    ),

    path(
        "cancel/<int:booking_id>/",
        views.cancel_booking,
        name="cancel_booking"
    ),

path(
    "review/<int:booking_id>/",
    views.add_review,
    name="add_review"
),
    # ==================================================
    # OWNER
    # ==================================================

    path(
        "owner-bookings/",
        views.owner_bookings,
        name="owner_bookings"
    ),

    path(
        "owner/details/<int:booking_id>/",
        views.owner_booking_details,
        name="owner_booking_details"
    ),

    path(
        "owner/approve/<int:booking_id>/",
        views.approve_booking,
        name="approve_booking"
    ),

    path(
        "owner/reject/<int:booking_id>/",
        views.reject_booking,
        name="reject_booking"
    ),

path(
    "owner/notifications/",
    views.owner_notifications,
    name="owner_notifications"
),
path(
    "owner/earnings/",
    views.owner_earnings,
    name="owner_earnings"
),
# ==================================================
    # admin
    # ==============
path(
   "bookings/admin_bookings.html",
   views.admin_bookings,
   name="admin_bookings"
),
path(
"bookings/admin_reviews.html",
   views.admin_reviews,
   name="admin_reviews"
),
   path(
        "delete-review/<int:review_id>/",
        views.delete_review,
        name="delete_review"
    ),
    # ==================================================
    # PAYMENT
    # ==================================================

    path(
        "payment/<int:booking_id>/",
        views.payment_page,
        name="payment_page"
    ),

    path(
        "payment/submit/<int:booking_id>/",
        views.submit_payment,
        name="submit_payment"
    ),

    path(
        "payment/wallet/<int:booking_id>/",
        views.wallet_payment,
        name="wallet_payment"
    ),

    # Owner verifies customer's UPI payment
    path(
        "owner/payment/verify/<int:booking_id>/",
        views.verify_payment,
        name="verify_payment"
    ),

    # Owner rejects customer's payment proof
    path(
        "owner/payment/reject/<int:booking_id>/",
        views.reject_payment,
        name="reject_payment"
    ),


    # ==================================================
    # COMPLETION
    # ==================================================

    path(
        "complete/<int:booking_id>/",
        views.complete_booking,
        name="complete_booking"
    ),


    # ==================================================
    # WALLET
    # ==================================================

    path(
        "wallet/",
        views.wallet,
        name="wallet"
    ),
    # ==================================================
# PAYMENT
# ==================================================

path(
    "payment/<int:booking_id>/",
    views.payment_page,
    name="payment_page"
),

path(
    "payment/submit/<int:booking_id>/",
    views.submit_payment,
    name="submit_payment"
),

path(
    "payment/wallet/<int:booking_id>/",
    views.wallet_payment,
    name="wallet_payment"
),

path(
    "payment-history/",
    views.payment_history,
    name="payment_history"
),

path(
    "owner/payment/verify/<int:booking_id>/",
    views.verify_payment,
    name="verify_payment"
),

path(
    "owner/payment/reject/<int:booking_id>/",
    views.reject_payment,
    name="reject_payment"
),
path(
        "download-receipt/<int:payment_id>/",
        views.download_receipt,
        name="download_receipt"
    ),




 path(
        "export-bookings-csv/",
        views.export_bookings_csv,
        name="export_bookings_csv"
    ),

path(
        "admin-booking-details/<str:invoice_number>/",
        views.admin_booking_details,
        name="admin_booking_details"
    ),
]