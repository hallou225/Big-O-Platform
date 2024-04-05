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

    student_id = request.user.id
    student_username = request.user.username
    student_password = request.user.password
    student_display_name = request.user.display_name
    student_first_name = request.user.first_name
    student_classes = request.user.student_class.all()

    context = {
        "student_id": student_id,
        "student_username": student_username,
        "student_password": student_password,
        "student_display_name": student_display_name,
        "student_first_name":student_first_name,
        "student_classes": student_classes
    }
    return render(request, 'student.html', context)

@login_required(login_url="/login")
def studentProfile(request):
    print("Student Views: def studentProfile(request):")
    if not isStudent(request):
        return redirect("/login")
    
    student = request.user
    context = {"student": student}

    return render(request, 'student_profile.html', context)

@login_required(login_url="/login")
def deleteStudentAccount(request):
    print("Student Views: def deleteStudentAccount(request):")
    if not isStudent(request):
        return redirect("/login")
    
    student = request.user
    
    if request.method == "POST":
        student.delete()
        return redirect("/login")

    context = {"student": student}

    return render(request, 'deleteStudentAccount.html', context)

@login_required(login_url="/login")
def updateStudentAccount(request):
    print("Student Views: def updateStudentAccount(request):")
    if not isStudent(request):
        return redirect("/login")
    
    student = request.user
    form = UpdateAccountForm(instance=student)

    if request.method == "POST":
        form = UpdateAccountForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("/student/profile")
 
    context = {"form": form, "student": student}
    return render(request, 'updateStudentAccount.html', context)

@login_required(login_url="/login")
def studentClass(request, class_pk):
    print("Student Views: def studentClass(request):")
    if not isStudent(request):
        return redirect("/login")
        
    student_class = Class.objects.get(id=class_pk)
    modules = student_class.module_set.all()

    '''
    algorithm_lines = {}
    for algorithm in module.algorithm_set.all():
        if algorithm.name not in algorithm_lines:
            algorithm_lines[algorithm.name] = []

        for line in algorithm.line_set.all():
            algorithm_lines[algorithm.name].append({
            'code': line.code,
            'answer': line.answer,
            'hint': line.hint
        })
    '''

    module_items = {}
    print("Number of modules: ", modules.count())
    for module in modules:
        if module.id not in module_items:
            module_items[module.id] = []
            
        items = module.item_set.all()
        print("Items: ", items)
        for item in items:

            module_items[module.id].append({
            'item_id': item.id,
            'item_name': item.name,
            'item_type': str(item.type)
        })

        print("item.type: ", type(str(item.type)))

        print("Item id: ", item.id)
        print("Item name: ", item.name)
    
    print("module_items: ", module_items)

    context = {"student_class": student_class, "modules": modules,
               "module_number": modules.count(), "module_items": module_items}
    return render(request, 'studentClass.html', context)

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

            if student in classToJoin.students.all():
                errorMessage = "You are already enrolled in this class."
            else:
                classToJoin.students.add(student)
                return redirect("/student")
        else:
            errorMessage = "There is no class with this class code."

    context = {"form": form, "errorMessage": errorMessage}
    return render(request, 'joinclass.html', context)

def leaveClass(request, class_pk):
    print("Student Views: def leaveClass(request):")
    if not isStudent(request):
        return redirect("/login")
        
    student_class = Class.objects.get(id=class_pk)

    if request.method == "POST":
        student_class.students.remove(request.user)
        return redirect("/student")

    context = {"student_class": student_class}
    return render(request, 'leaveClass.html', context)

@login_required(login_url="/login")
def studentModule(request, class_pk, module_pk):
    print("Student Views: def studentModule(request):")
    if not isStudent(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    
    context = {"student_class": student_class, "module": module}

    return render(request, 'studentModule.html', context)

@login_required(login_url="/login")
def algorithm(request, class_pk, module_pk, item_pk):
    print("Student Views: def algorithm(request):")
    if not isStudent(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    algorithm = Algorithm.objects.get(id=item_pk)

    context = {"student_class": student_class, "module": module, "algorithm": algorithm}

    return render(request, 'studentAlgorithm.html', context)

@login_required(login_url="/login")
def page(request, class_pk, module_pk, item_pk):
    print("Student Views: def page(request):")
    if not isStudent(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    page = Page.objects.get(id=item_pk)

    context = {"student_class": student_class, "module": module, "page": page}

    return render(request, 'studentPage.html', context)