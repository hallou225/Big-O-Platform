from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup, name="signup"),
    path("", views.signup2, name="signup2")
]