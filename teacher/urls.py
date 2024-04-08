from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher, name="teacher"),
    path("createClass/", views.createClass, name="createClass"),
    path("profile/", views.profile, name="profile"),
    path("profile/updateTeacherAccount/", views.updateTeacherAccount, name="updateTeacherAccount"),
    path("profile/deleteTeacherAccount/", views.deleteTeacherAccount, name="deleteTeacherAccount"),
    path("class/<str:class_pk>/", views.teacherClass, name="teacherClass"),
    path("createClass/", views.createClass, name="createClass"),
    path("class/<str:class_pk>/deleteClass/", views.deleteClass, name="deleteClass"),
    path("class/<str:class_pk>/updateClass/", views.updateClass, name="updateClass"),  
    path("class/<str:class_pk>/createModule/", views.createModule, name="createModule"),
    path("class/<str:class_pk>/module/<str:module_pk>/", views.module, name="module"),
    path("class/<str:class_pk>/module/<str:module_pk>/", views.module, name="module"),
    path("class/<str:class_pk>/deleteModule/<str:module_pk>/", views.deleteModule, name="deleteModule"),
    path("class/<str:class_pk>/updateModule/<str:module_pk>/", views.updateModule, name="updateModule"),
    path("class/<str:class_pk>/module/<str:module_pk>/algorithm/", views.algorithm, name="algorithm"),
    path("class/<str:class_pk>/module/<str:module_pk>/createAlgorithm", views.createAlgorithm, name="createAlgorithm"),
    path("class/<str:class_pk>/module/<str:module_pk>/deleteAlgorithm/<str:algorithm_pk>", views.deleteAlgorithm, name="deleteAlgorithm"),
    path("class/<str:class_pk>/module/<str:module_pk>/createPage", views.createPage, name="createPage"),
    path("class/<str:class_pk>/module/<str:module_pk>/deletePage/<str:page_pk>", views.deletePage, name="deletePage"),


    path("class/<str:class_pk>/modules/", views.modules, name="modules"),
    path("class/<str:class_pk>/pages/<page_pk>", views.teacherViewPage, name="teacherViewPage"),
    path("class/<str:class_pk>/algorithms/<algorithm_pk>", views.teacherViewAlgorithm, name="teacherViewAlgorithm"),

]