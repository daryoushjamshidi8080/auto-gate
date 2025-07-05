from django.urls import path
from . import views


app_name = 'rule'
urlpatterns = [
    path('', views.RuleView.as_view(), name='show_rule'),
    path('show-list-rule/', views.ListRuleView.as_view(), name='rule-list'),
    path('delete-rule/', views.DeleteRuelView.as_view(), name='rule-delete'),
    path('create-rule/', views.CreateRuleView.as_view(), name='rule-create'),
    path('update-rule/<int:rule_id>/',
         views.UpdateRuleView.as_view(), name='rule-update'),

]
