from django.urls import path
from . import views


urlpatterns = [
    path("", views.Home.as_view() ,name='home'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("register/", views.register_user, name='register'),
    path("record/detail/<int:pk>", views.RecordDetail.as_view(), name='record'),
    path("record/delete/<int:pk>", views.delete_record, name='delete_record'),
    path("record/add", views.AddRecord.as_view(), name='add_record'),
    path("record/update/<int:pk>", views.UpdateRecord.as_view(), name='update_record'),
    path("groups/add", views.CreateUserGroup.as_view(), name='create_group'),
    path("groups/view", views.UserGroupLists.as_view(), name='view_groups'),
    #path("groups/detail", views..as_view(), name='detail_group'),
    #path("groups/delete", views..as_view(), name='delete_group'),
]