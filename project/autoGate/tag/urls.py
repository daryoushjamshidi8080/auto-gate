from django.urls import path
from . import views


app_name = "tag"
urlpatterns = [
    path("", views.TagView.as_view(), name="tag"),
    path("list-tag/", views.ListTagView.as_view(), name="tag-list"),
    path("add-tag/", views.AddTagView.as_view(), name="tag-create"),
]