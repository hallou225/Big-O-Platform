from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup2, name="signup2"),
    path("", views.home, name="home")
]