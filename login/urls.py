from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginBase, name="loginBase"),
    path("teacher/", views.teacher, name="teacher"),
    path("register/", views.register, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout")
]