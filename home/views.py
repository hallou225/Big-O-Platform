from urllib.request import Request
from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def teacher(request):
    return render(request, 'teacher.html')

def signup(request):
    return render(request, 'signup.html')