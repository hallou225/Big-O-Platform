from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *
from django.http import HttpResponse
from markdownx.utils import markdown

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
    student_modules = student_class.module_set.all()

    items = Item.objects.none()
    algorithms = Algorithm.objects.none()
    pages = Page.objects.none()

    for module in student_modules:
        module_items = Item.objects.filter(module=module)
        items = items.union(module_items)

    for item in items:
        item_pages = Page.objects.filter(item=item)
        pages = pages.union(item_pages)
        
        item_algorithms = Algorithm.objects.filter(item=item)
        algorithms = algorithms.union(item_algorithms)

    print("items: ", items)
    for item in items:
        print("item.module: ", item.module)
    
    print()

    print("algorithms: ", algorithms)
    for algorithm in algorithms:
        print("algorithm: ", algorithm)
    
    print()

    print("pages: ", pages)
    for page in pages:
        print("page: ", page)
    
    print()

    for module in student_modules:
        print("module.name: ", module.name)
        for item in items:
            if module.name == item.module.name:
                print("item.module: ", item.module)
            
    context = {"student_class": student_class, "modules": student_modules,
                "module_number": student_modules.count(), "items": items,
                "algorithms": algorithms, "pages": pages}
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
def algorithm(request, class_pk, module_pk, algorithm_pk):
    print("Student Views: def algorithm(request):")
    if not isStudent(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    algorithm = Algorithm.objects.get(id=algorithm_pk)
    codes = algorithm.lines.split("\n")
    answers = algorithm.answers.split("\n")
    hints = algorithm.hints.split("\n")

    # Retrieving the answers submitted by the student and calculate the grade
    score = 0
    lineStatus = []
    studentAnswers = []
    if request.method == 'POST':
        studentAnswers = request.POST.getlist('answers[]')
        for i in range(len(codes)):
            # If student answers (the current line in iteration) correctly
            if answers[i] == studentAnswers[i]:  # Correct
                score += 1
                lineStatus.append(True)
            else:                              # Incorrect
                lineStatus.append(False)
    
    results = zip(lineStatus, codes, studentAnswers, hints)
    # print("\n zip result \n")
    # for s, c, sa, h in results:
    #     print(f"| {s} | {c} | {sa} | {h} |")

    total = len(codes)
    percentage = (score / total) * 100
    percentage = round(percentage, 2)
    score = f"{score}/{total}"
    percentage = f"{percentage}%"

    context = {"student_class": student_class, "module": module, "algorithm": algorithm,
            "codes": codes, "answers": answers, 
            "score": score, "percentage": percentage , "lineStatus": lineStatus, "results": results}
    return render(request, 'studentAlgorithm.html', context)


@login_required(login_url="/login")
def page(request, class_pk, module_pk, page_pk):
    print("Student Views: def page(request):")
    if not isStudent(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    page = Page.objects.get(id=page_pk)
    page.content = markdown(page.content, extensions=['extra'])

    context = {"student_class": student_class, "module": module, "page": page}
    return render(request, 'studentPage.html', context)