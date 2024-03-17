from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher, name="teacher"),
    path("createclass/", views.createclass, name="createclass"),
    path("profile/", views.profile, name="profile"),
    path("class/<str:class_pk>/", views.teacherClass, name="teacherClass"),
]