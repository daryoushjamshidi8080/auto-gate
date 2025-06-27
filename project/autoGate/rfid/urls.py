from django.urls import path
from . import views

app_name = "rfid"
urlpatterns = [
    path("read_tag/", views.ReadTag.as_view(), name="read_tag"),
    path("start-thread/", views.StartThread.as_view(), name="start_thread"),
    path('stop-thread/', views.StopThread.as_view(), name='stop_thread')
]
