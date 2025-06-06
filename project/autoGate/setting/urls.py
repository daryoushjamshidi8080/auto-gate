from django.urls import path
from . import views

app_name = "setting"
urlpatterns = [
    path("", views.SettingView.as_view(), name="setting"),
    path("create-antenna/", views.CreateAntennaView.as_view(), name="create_antenna"),
    path("antenna-list/", views.AntennaListPartialView.as_view(), name="antenna_list_partial"), 
    path("delete-antenna/<int:antenna_id>/", views.DeleteAntennaView.as_view(), name="delete_antenna"),
    path('update-antenna/<int:antenna_id>/', views.UpdateAntennaView.as_view(), name='update_antenna'),
    path('user-list/', views.UserListPartialView.as_view(), name='user_list_partial'),
    path('create-user/', views.CreateUserView.as_view(), name='create_user'),
    path('delete-user/<int:user_id>/', views.DeleteUserView.as_view(), name='delete_user'),
]