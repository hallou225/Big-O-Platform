from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *
from django.http import HttpResponse
from markdownx.utils import markdown
import ast
from django.http import JsonResponse
from django.urls import reverse
import json
from django.contrib import messages

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
            messages.success(request, 'Account updated successfully')
            url = reverse("studentProfile")
            return redirect(url)
            # return redirect("/student/profile")
 
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
                messages.success(request, 'Joined class successfully')
                url = reverse("studentClass", kwargs={"class_pk":classToJoin.id})
                return redirect(url)
                # return redirect("/student")
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
        messages.success(request, 'Class unenrolled successfully')
        url = reverse("student")
        return redirect(url)
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

    # If there's a previous answer stored in the database for this student and this algorithm...
    else:
        try:
            student_algorithm = StudentAlgorithm.objects.get(student=request.user.id, algorithm=algorithm_pk)
            studentAnswers = ast.literal_eval(student_algorithm.answers)
            print(f"type(studentAnswers): {type(studentAnswers)}")
            print(f"studentAnswers: {studentAnswers}")
            for i in range(len(codes)):
                # If student answers (the current line in iteration) correctly
                if answers[i] == studentAnswers[i]:  # Correct
                    score += 1
                    lineStatus.append(True)
                else:                              # Incorrect
                    lineStatus.append(False)
        except:
            pass
        
    
    results = zip(lineStatus, codes, studentAnswers, hints)
    # print("\n zip result \n")
    # for s, c, sa, h in results:
    #     print(f"| {s} | {c} | {sa} | {h} |")

    total = len(codes)
    percentage = (score / total) * 100
    percentage = round(percentage, 2)
    score = f"{score}/{total}"
    percentage = f"{percentage}%"

    ###################################### Save the student's submission in the database ######################################

    # If the student has never submitted for this algorithm...

    try:
        student_algorithm = StudentAlgorithm.objects.get(student=request.user.id, algorithm=algorithm_pk)
        # Student has ALREADY submitted for this algorithm...
        print("STUDENT HAS ALREADY SUBMITTED FOR THIS ALGORITHM BEFORE")

        # Storing answers, score, and percentage in the database
        student_algorithm.answers = studentAnswers
        student_algorithm.score = score
        student_algorithm.percentage = percentage
        student_algorithm.save()

    except:
        # Student has NEVER submitted for this algorithm before...
        print("STUDENT HAS NEVER SUBMITTED BEFORE")

        # Creating a new instance of the StudentAlgorithm model
        student_algorithm = StudentAlgorithm(
            student_id = request.user.id, algorithm_id = algorithm_pk,
            answers = studentAnswers, score = score, percentage = percentage
        )
        student_algorithm.save()

        # student_algorithm = StudentAlgorithm()
        # student_algorithm.student_id = request.user.id
        # student_algorithm.algorithm_id = algorithm_pk
        # student_algorithm.answers = studentAnswers
        # student_algorithm.score = score
        # student_algorithm.percentage = percentage
        # student_algorithm.save()

        # student_algorithm = StudentAlgorithm.objects.create(
        #     student_id = request.user.id, algorithm_id = algorithm_pk,
        #     answers = studentAnswers, score = score, percentage = percentage
        # )

    ###########################################################################################################################

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

@login_required(login_url="/login")
def studentModules(request, class_pk):
    print("\nStudent Views: def studentModules(request):\n-----------------------------------------------")
    if not isStudent(request):
        return redirect("/login")

    student_class = Class.objects.get(id=class_pk)
    student_modules = student_class.module_set.all()

    if request.method == 'POST':
        orderDict = request.POST.get('orderDict') 

        context = {
            "student_class": student_class
        }
        
        if orderDict:
            try:
                # Convert string representation to dictionary
                orderDict = json.loads(orderDict)  
                # Parse the order dictionary and update every module that matches the obj_id
                for obj_id, new_order in orderDict.items():  
                    obj = Module.objects.get(pk=obj_id)
                    obj.order = new_order
                    obj.save()
                    
                url = reverse("studentModules", kwargs={"class_pk":student_class.id})
                return redirect(url)   
                #return JsonResponse({'success': True})
            
            except Module.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Object not found'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No data provided'})
    else:
        items = Item.objects.none()
        algorithms = Algorithm.objects.none()
        pages = Page.objects.none()
        empty_modules = Module.objects.none()
        for module in student_modules:
            # return all items of this module
            module_items = Item.objects.filter(module=module)
            
            # if items are returned append to the items query set
            if module_items.exists():            
                items = items.union(module_items)
            else: # else, if no items are returned, add the module to the empty_modules queryset
                empty_modules = empty_modules | Module.objects.filter(id=module.id)

        # create a query set for the pages and algorithms that matches the items in the items queryset
        for item in items:
            item_pages = Page.objects.filter(item=item)
            pages = pages.union(item_pages)
            
            item_algorithms = Algorithm.objects.filter(item=item)
            algorithms = algorithms.union(item_algorithms)
        
        # Order the list of modules and items by order
        student_modules = student_modules.order_by('order')
        items = items.order_by('order')
        context = {
            "student_class": student_class,
            "modules": student_modules,
            "empty_modules": empty_modules,
            "module_number": student_modules.count(),
            "items": items,
            "algorithms": algorithms,
            "pages": pages
        }

        return render(request, 'studentModules.html', context)
