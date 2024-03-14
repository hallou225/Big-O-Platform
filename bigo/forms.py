from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import User

from _database.models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "middle_name", "last_name", "display_name", "username", "email", "password1", "password2"]