from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher, name="teacher"),
    path("createclass/", views.createclass, name="createclass"),
    path("profile/", views.profile, name="profile"),
    path("profile/updateTeacherAccount/", views.updateTeacherAccount, name="updateTeacherAccount"),
    path("profile/deleteTeacherAccount/", views.deleteTeacherAccount, name="deleteTeacherAccount"),
    path("class/<str:class_pk>/", views.teacherClass, name="teacherClass"),
    path("class/<str:class_pk>/deleteClass/", views.deleteClass, name="deleteClass"),
    path("class/<str:class_pk>/updateClass/", views.updateClass, name="updateClass"),  
    path("class/<str:class_pk>/createModule/", views.createModule, name="createModule"),
    path("class/<str:class_pk>/module/<str:module_pk>/", views.module, name="module"),
    path("class/<str:class_pk>/module/<str:module_pk>/algorithm/", views.algorithm, name="algorithm"),
    
]