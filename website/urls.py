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
]