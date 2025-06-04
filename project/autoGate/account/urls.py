from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="account-login"),
    path("logout/", views.UserLogoutView.as_view(), name="account-logout"),
]
