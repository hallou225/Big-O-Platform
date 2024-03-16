from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher, name="teacher"),
    path("createclass/", views.createclass, name="createclass"),
    path("profile/", views.profile, name="profile"),
    path("class/", views.teacherClass, name="class"),
]