from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *
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
            
    #     items = module.item_set.all()
    #     print("Items: ", items)
    #     for item in items:

    #         module_items[module.id]["items"].append({
    #         'item_id': item.id,
    #         'item_name': item.name,
    #         'item_type': str(item.type),
    #         "module_name": module.name,
    #     })

    #     print("item.type: ", type(str(item.type)))

    #     print("Item id: ", item.id)
    #     print("Item name: ", item.name)
    
    # print("module_items: ", module_items)

    '''context = {"student_class": student_class, "modules": student_modules,
               "module_number": student_modules.count(), "modulesDict": modulesDict,
               "itemsDict": itemsDict, "pages": pages, "algorithms": algorithms}'''
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
    if not isStudentHenri(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    algorithmHenri = Algorithm.objects.get(id=algorithm_pk)
    
    lines = algorithm.line_set.all()
    print("lines: ", lines)

    for line in lines:
        print("line: ", line.code, "|", line.answer, "|", line.hint)

    print("algorithm_pk: ", algorithm_pk)

    # Retrieving the answers submitted by the student
    scores = {}
    algorithm_score = 0
    if request.method == 'POST':
        answers = request.POST.getlist('answers[]')
        print("answers:", answers)

        for i in range(len(lines)):
            print(f"Line {i}:")
            print(f"Student's Answer: {answers[i]}")
            print(f"Correct Answer: {lines[i].answer}")

            # If student answers (the current line in iteration) correctly
            if answers[i] == lines[i].answer:
                scores[f"Line {i}"] = 1     # Correct
                algorithm_score += 1
            else:
                scores[f"Line {i}"] = 0     # Incorrect
        
        print(f"scores: {scores}")  # Scores for each line
        print(f"algorithm_score: {algorithm_score}")   # Total score for algorithm

    contextHenri = {"student_class": student_class, "module": module, "algorithm": algorithm,
               "lines": lines, "scores": scores.items(), "algorithm_score": algorithm_score}

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

@login_required(login_url="/login")
def item(request, class_pk, module_pk, item_pk):
    print("Student Views: def item(request):")
    if not isStudent(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    item = Item.objects.get(id=item_pk)

    print("item_pk: ", item_pk)

    context = {"student_class": student_class, "module": module, "item": item}

    print("-------item.type: ", item.type)

    if str(item.type) == "Algorithm":
        #algorithm = Algorithm.objects.get(id=item_pk)
        #context = {"student_class": student_class, "module": module, "algorithm": algorithm}
        return render(request, 'studentAlgorithm.html', context)
    elif str(item.type) == "Page":
        #page = Page.objects.get(id=item_pk)
        #context = {"student_class": student_class, "module": module, "page": page}
        return render(request, 'studentPage.html', context)

    # return render(request, 'studentItem.html', context)
