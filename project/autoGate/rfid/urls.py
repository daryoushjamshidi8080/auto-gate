from django.urls import path
from . import views

app_name = "rfid"
urlpatterns = [
    path("read_tag/", views.ReadTag.as_view(), name="read_tag"),
]
