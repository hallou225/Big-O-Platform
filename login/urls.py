from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginBase, name="loginBase"),
    path("register/", views.register, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("bootstrap/", views.bootstrap, name="bootstrap"),
    path("test_code/", views.test_code, name="test_code"),
]