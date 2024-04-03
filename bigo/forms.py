from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from _database.models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ["first_name", "middle_name", "last_name", "display_name", "username", "email", "password1", "password2"]

class CreateClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'term', 'class_code', 'language']
        widgets = {
            'term': forms.Select(attrs={'class': 'textEntry'}),
            'language': forms.Select(attrs={'class': 'textEntry'})
        }

class JoinClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['class_code']

<<<<<<< HEAD
=======
class JoinClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['class_code']

>>>>>>> cc5a1c0757f9d462a9f32108ace5ed7ae915ea53
class CreateModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = '__all__'

class AlgorithmForm(ModelForm):
    class Meta:
        model = Algorithm
        fields = '__all__'

class UpdateAccountForm(ModelForm):
    class Meta:
        model = Account
<<<<<<< HEAD
        fields = ['first_name', 'middle_name', 'last_name', 'display_name', 'role', 'email']
=======
        fields = ['first_name', 'middle_name', 'last_name', 'display_name', 'email']
>>>>>>> cc5a1c0757f9d462a9f32108ace5ed7ae915ea53
