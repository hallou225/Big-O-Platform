from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *
from django.contrib.auth import get_user_model

# Create your views here.


@login_required(login_url="/login")
def teacher(request):
    return render(request, 'teacher.html')

@login_required(login_url="/login")
def createclass(request):
    form = CreateClassForm()
    if request.method == "POST":
        form = CreateClassForm(request.POST)
        if form.is_valid():
            teacher = request.user

            '''
            teacher_id = request.user.id
            teacher_username = request.user.username
            teacher_password = request.user.password
            '''

            new_class = form.save(commit=False)
            new_class.teacher = teacher
            new_class.save()

            return redirect("/teacher")
    
    context = {"form": form}
    return render(request, 'createclass.html', context)

@login_required(login_url="/login")
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url="/login")
def teacherClass(request):
    return render(request, 'class.html')
