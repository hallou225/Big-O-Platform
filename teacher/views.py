from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login")
def teacher(request):
    return render(request, 'teacher.html')

@login_required(login_url="/login")
def createclass(request):
    return render(request, 'createclass.html')

@login_required(login_url="/login")
def profile(request):
    return render(request, 'profile.html')
