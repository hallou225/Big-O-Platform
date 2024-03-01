from django.shortcuts import render

# Create your views here.

def createclass(request):
    return render(request, 'createclass.html')

def teacher(request):
    return render(request, 'teacher.html')
