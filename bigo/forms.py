"""@package docstring
Documentation for this module.

More details.
"""

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from _database.models import *

class CreateUserForm(UserCreationForm):
    """Documentation for the CreateUserForm class.
    
    More details.
    """
    class Meta:
        """Documentation for the Meta class.
    
        More details.
        """
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

class JoinClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['class_code']

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
        fields = ['first_name', 'middle_name', 'last_name', 'display_name', 'email']

class CreatePageForm(ModelForm):
    class Meta:
        model = Page
        fields = '__all__'