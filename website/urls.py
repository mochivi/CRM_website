from django.urls import path
from . import views


urlpatterns = [
    path("", views.Home.as_view() ,name='home'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("register/", views.register_user, name='register'),
    path("record/<int:pk>", views.RecordDetail.as_view(), name='record')
]