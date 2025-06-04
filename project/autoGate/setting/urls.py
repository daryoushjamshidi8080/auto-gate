from django.urls import path
from . import views

app_name = "setting"
urlpatterns = [
    path("", views.SettingView.as_view(), name="setting"),
    path("create-antenna/", views.CreateAntennaView.as_view(), name="create_antenna"),
]