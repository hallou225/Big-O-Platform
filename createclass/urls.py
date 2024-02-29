from django.urls import path
from . import views

urlpatterns = [
    path("", views.createclass, name="createclass"),
    path("", views.teacher, name="teacher")
]
