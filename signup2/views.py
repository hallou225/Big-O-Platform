from django.shortcuts import render, HttpResponse

# Create your views here.

def signup2(request):
    return render(request, 'signup2.html')

def home(request):
    return render(request, 'home.html')
