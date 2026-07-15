from django.urls import path
from . import views

urlpatterns = [

    path("signup/", views.signup, name="signup"),

    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),

    path("customer/profile/",views.customer_profile,name="customer_profile"),

    path("owner/profile/",views.owner_profile,name="owner_profile"),

]