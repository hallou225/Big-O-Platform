from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from _database.models import *

class TeacherBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Teacher.objects.get(username=username)
            if user.check_password(password):
                return user
        except Teacher.DoesNotExist:
            return None

        return None
