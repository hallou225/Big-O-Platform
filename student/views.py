from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *

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
    print("Student Views: def student(request):")
    if not isStudent(request):
        return redirect("/login")
    return render(request, 'student.html')

@login_required(login_url="/login")
def profile(request):
    print("Student Views: def profile(request):")
    if not isStudent(request):
        return redirect("/login")
    
    student = request.user
    context = {"student": student}

    return render(request, 'student_profile.html', context)

@login_required(login_url="/login")
def joinclass(request):
    print("Student Views: def joinclass(request):")
    if not isStudent(request):
        return redirect("/login")
    
    errorMessage = ""
    form = JoinClassForm()

    if request.method == "POST":
        form = JoinClassForm(request.POST)
        if form.is_valid():
            try:
                class_code = form.cleaned_data["class_code"]
                class_to_join = Class.objects.get(class_code=class_code)
                student = request.user
                class_to_join.students.add(student)
                print("Redirect to other page......")
                return redirect("/student")
            except Class.DoesNotExist:
                print("No class with that code......")
                errorMessage = "There is no class with this class code."


    context = {"form": form, "errorMessage": errorMessage}
    return render(request, 'joinclass.html', context)


@login_required(login_url="/login")
def joinclass(request):
    print("Student Views: def joinclass(request):")
    if not isStudent(request):
        return redirect("/login")
    
    errorMessage = ""
    form = JoinClassForm()

    if request.method == "POST":
        form = JoinClassForm(request.POST)

        class_code = request.POST.get("class_code")
        
        classesWithCode = Class.objects.filter(class_code=class_code)
        
        if classesWithCode.exists():
            classToJoin = classesWithCode.first()
            student = request.user._wrapped
            classToJoin.students.add(student)
            errorMessage = "Students in this class: "
            return redirect("/student")
        else:
            errorMessage = "There is no class with this class code."

    context = {"form": form, "errorMessage": errorMessage}
    return render(request, 'joinclass.html', context)