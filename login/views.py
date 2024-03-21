from urllib.request import Request
from django.shortcuts import render, HttpResponse, redirect
from _database.models import *

from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect

from bigo.forms import *
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from bigo.forms import CreateUserForm
from django.contrib.auth import get_user_model

# Create your views here.

def loginBase(request):
    print("Login Views: def loginBase(request):")
    return redirect("/login")

@csrf_protect
def register(request):
    print("Login Views: def register(request):")
    if request.user.is_authenticated:
        return redirect("/teacher")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")

                new_teacher = get_user_model().objects.create_user(
                    first_name=form.cleaned_data.get("first_name"),
                    middle_name=form.cleaned_data.get("middle_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    display_name=form.cleaned_data.get("display_name"),
                    username=username,
                    password=password,
                    email=form.cleaned_data.get("email"),
                )

                messages.success(request, "Account was created for " + username)

                return redirect("/login")

    context = {"form": form}
    return render(request, 'register.html', context)

def loginPage(request):
    print("Login Views: def loginPage(request):")
    if request.user.is_authenticated:
        if str(request.user.role) == "Teacher":
            return redirect("/teacher")
        elif str(request.user.role) == "Student":
            return redirect("/student")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if isinstance(user, Account):
                    login(request, user)
                    print("request.user.role: ", str(request.user.role))
                    if str(request.user.role) == "Teacher":
                        return redirect("/teacher")
                    elif str(request.user.role) == "Student":
                        return redirect("/student")
            else:
                messages.info(request, "Username OR password is incorrect")

        return render(request, 'login.html')

def logoutUser(request):
    print("Login Views: def logoutUser(request):")
    logout(request)
    return redirect("/login")
