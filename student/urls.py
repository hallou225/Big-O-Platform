from django.urls import path
from . import views

urlpatterns = [
    path("", views.student, name="student"),
    path("joinclass/", views.joinclass, name="joinclass"),
    path("profile/", views.profile, name="profile"),
    path("class/<str:class_pk>/", views.studentClass, name="studentClass"),
    path("class/<str:class_pk>/leaveClass/", views.leaveClass, name="leaveClass"),
    path("class/<str:class_pk>/module/<str:module_pk>/", views.studentModule, name="studentModule"),
]

'''
path("class/<str:class_pk>/module/<str:module_pk>/", views.module, name="module"),
path("class/<str:class_pk>/module/<str:module_pk>/algorithm/", views.algorithm, name="algorithm"),
'''