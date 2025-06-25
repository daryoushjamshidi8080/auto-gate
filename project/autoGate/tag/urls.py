from django.urls import path
from . import views


app_name = "tag"
urlpatterns = [
    path("", views.TagView.as_view(), name="tag"),
    path("list-tag/", views.ListTagView.as_view(), name="tag-list"),
    path("add-tag/", views.AddTagView.as_view(), name="tag-create"),
    path('list_tag_anonymous/', views.TagAnonymous.as_view(), name='tag-anonymous'),
    path('delete-tag/<int:tag_id>/',
         views.DeleteTagView.as_view(), name='tag-delete')
]
