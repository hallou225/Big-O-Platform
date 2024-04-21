from django.urls import path
from . import views

urlpatterns = [

    # Home Page
    path("", views.teacher, name="teacher"),

    # Teacher's Profile CRUD
    path("profile/", views.profile, name="profile"),
    path("profile/updateTeacherAccount/", views.updateTeacherAccount, name="updateTeacherAccount"),
    path("profile/deleteTeacherAccount/", views.deleteTeacherAccount, name="deleteTeacherAccount"),

    # Class CRUD
    path("createClass/", views.createClass, name="createClass"),
    path("class/<str:class_pk>/updateClass/", views.updateClass, name="updateClass"),  
    path("class/<str:class_pk>/deleteClass/", views.deleteClass, name="deleteClass"),
    path("class/<str:class_pk>/", views.teacherClass, name="teacherClass"),

    # Module CRUD
    path("class/<str:class_pk>/createModule/", views.createModule, name="createModule"),
    path("class/<str:class_pk>/updateModule/<str:module_pk>/", views.updateModule, name="updateModule"),
    path("class/<str:class_pk>/deleteModule/<str:module_pk>/", views.deleteModule, name="deleteModule"),
    path("class/<str:class_pk>/modules/", views.modules, name="modules"),
    path("class/<str:class_pk>/modules/<str:module_pk>/", views.manageModule, name="manageModule"),

    # Algorithm CRUD
    path("class/<str:class_pk>/module/<str:module_pk>/createAlgorithm", views.createAlgorithm, name="createAlgorithm"),
    path("class/<str:class_pk>/algorithms/<str:algorithm_pk>/update", views.updateAlgorithm, name="updateAlgorithm"),
    path("class/<str:class_pk>/algorithms/<str:algorithm_pk>/deleteAlgorithm>", views.deleteAlgorithm, name="deleteAlgorithm"),
    path("class/<str:class_pk>/algorithms/<str:algorithm_pk>", views.teacherViewAlgorithm, name="teacherViewAlgorithm"),

    # Page CRUD
    path("class/<str:class_pk>/module/<str:module_pk>/createPage", views.createPage, name="createPage"),
    path("class/<str:class_pk>/pages/<page_pk>/update", views.updatePage, name="updatePage"),
    path("class/<str:class_pk>/Pages/<str:page_pk>/delete", views.deletePage, name="deletePage"),
    path("class/<str:class_pk>/pages/<page_pk>", views.teacherViewPage, name="teacherViewPage"),

]