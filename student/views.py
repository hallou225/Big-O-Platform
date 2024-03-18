from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def isStudent(request):
    print("checkRole function")
    if request.user.is_authenticated:
        print("request.user.role: ", str(request.user.role))
        if str(request.user.role) == "Student":
            return True
        else:
            print("redirect to /login")
            return False

@login_required(login_url="/login")
def student(request):
    if not isStudent(request):
        return redirect("/login")
    return render(request, 'student.html')