from django.urls import path
from . import views

urlpatterns = [
    path("1/", views.signup, name="signup"),
    path("2/", views.signup2, name="signup2")
]