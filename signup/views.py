from django.shortcuts import render, HttpResponse

# Create your views here.

def signup(request):
    return render(request, 'signup.html')

def signup2(request):
    return render(request, 'signup2.html')
