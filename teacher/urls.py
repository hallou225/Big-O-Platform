from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher, name="teacher"),
    path("", views.createclass, name="createclass")
]