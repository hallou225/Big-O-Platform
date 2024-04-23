from django.urls import path
from . import views

urlpatterns = [
    path("", views.student, name="student"),
    path("joinclass/", views.joinclass, name="joinclass"),
    path("profile/", views.studentProfile, name="studentProfile"),
    path("profile/updateStudentAccount/", views.updateStudentAccount, name="updateStudentAccount"),
    path("profile/deleteStudentAccount/", views.deleteStudentAccount, name="deleteStudentAccount"),
    path("class/<str:class_pk>/", views.studentClass, name="studentClass"),
    path("class/<str:class_pk>/leaveClass/", views.leaveClass, name="leaveClass"),
    path("class/<str:class_pk>/module/<str:module_pk>/", views.studentModule, name="studentModule"),

    path("class/<str:class_pk>/module/<str:module_pk>/algorithm/<str:algorithm_pk>/", views.algorithm, name="studentAlgorithm"),
    path("class/<str:class_pk>/module/<str:module_pk>/page/<str:page_pk>/", views.page , name="studentPage"),
    path("class/<str:class_pk>/studentModules/", views.studentModules, name="studentModules"),
]

'''
path("class/<str:class_pk>/module/<str:module_pk>/algorithm/", views.algorithm, name="algorithm"),
'''