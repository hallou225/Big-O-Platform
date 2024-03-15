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
            form.save()
            return redirect("/teacher")
    
    context = {"form": form}
    return render(request, 'createclass.html', context)

@login_required(login_url="/login")
def profile(request):
    return render(request, 'profile.html')
