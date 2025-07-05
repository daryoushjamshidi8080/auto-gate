from django.urls import path
from . import views


app_name = "logs"

urlpatterns = [
    path("", views.LogsView.as_view(), name="logs"),
    path('show-list/', views.ShowLogsView.as_view(), name='show_logs')
]
