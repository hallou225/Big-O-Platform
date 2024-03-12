from django.shortcuts import render

# Create your views here.

def teacher(request):
    return render(request, 'teacher.html')

def createclass(request):
    return render(request, 'createclass.html')

def profile(request):
    return render(request, 'profile.html')
