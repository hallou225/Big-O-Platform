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
    '''
    students = Student.objects.all()
    teachers = Teacher.objects.all()

    #students_usernames_and_passwords = list(students.values('username', 'password'))
    student_data = list(students.values("username", "password"))
    teacher_data = list(teachers.values("username", "password"))

    total_students = students.count()
    total_teachers = teachers.count()

    context = {
        "students": students,
        "teachers": teachers,
        "total_students": total_students,
        "total_teachers": total_teachers
        }

    return render(request, 'home.html', context)
    '''
    # return render(request, 'home.html')
    return redirect("/login")

@login_required(login_url="/login")
def teacher(request):
    return render(request, 'teacher.html')

'''
@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return redirect("/teacher")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)

                return redirect("/login")

    context = {"form": form}
    return render(request, 'signup.html', context)
'''

'''
@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return redirect("/teacher")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                # Extract the username and password from the form
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")

                # Create a new Teacher instance with the provided data
                new_teacher = Teacher.objects.create(
                    first_name=form.cleaned_data.get("first_name"),
                    middle_name=form.cleaned_data.get("middle_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    display_name=form.cleaned_data.get("display_name"),
                    username=username,
                    password=password,
                    email=form.cleaned_data.get("email"),
                )

                messages.success(request, "Account was created for " + username)

                print("Signup username: ", username)
                print("Signup password: ", password)

                return redirect("/login")

    context = {"form": form}
    return render(request, 'signup.html', context)
'''

@csrf_protect
def register(request):
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
    if request.user.is_authenticated:
        return redirect("/teacher")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            print("Login username: ", username)
            print("Login password: ", password)

            user = authenticate(request, username=username, password=password)

            print("User after authentication:", user)

            if user is not None:
                if isinstance(user, Teacher):
                    login(request, user)
                    '''
                    next_url = request.GET.get('next', '/teacher/')
                    return redirect(next_url)
                    '''
                    return redirect("/teacher")
                else:
                    messages.info(request, "You do not have permission to log in as a teacher.")
            else:
                messages.info(request, "Username OR password is incorrect")

        return render(request, 'login.html')

'''
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("/teacher")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if the user is a teacher
                if user.teacher:
                    login(request, user)
                    return redirect("/teacher")
                else:
                    messages.info(request, "You do not have permission to log in as a teacher.")
            else:
                messages.info(request, "Username OR password is incorrect")

        return render(request, 'login.html')
'''

def logoutUser(request):
    logout(request)
    return redirect("/login")
