from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse
import json
import re
from django.contrib import messages



def clean_answer(text):
    # Remove leading and trailing whitespaces and newlines
    text = text.strip()

    # Remove newlines
    #text = text.replace('\n', '')

    # Remove all spaces between words
    text = re.sub(r'\s+', '', text)
    return text


# Create your views here.
def isTeacher(request):
    """! The isTeacher class.
    Checks the role of the user trying to access a page
    """
    print("checkRole function")
    if request.user.is_authenticated:
        print("request.user.role: ", str(request.user.role), "\n")
        if str(request.user.role) == "Teacher":
            return True
        else:
            print("redirect to /login")
            return False

@login_required(login_url="/login")
def teacher(request):
    print("\nTeacher Views: def teacher(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_id = request.user.id
    teacher_username = request.user.username
    teacher_password = request.user.password
    teacher_display_name = request.user.display_name
    teacher_first_name = request.user.first_name
    
    teacher_classes = Class.objects.filter(teacher_id=teacher_id)
    

    context = {
        "teacher_id": teacher_id,
        "teacher_username": teacher_username,
        "teacher_password": teacher_password,
        "teacher_display_name": teacher_display_name,
        "teacher_first_name":teacher_first_name,
        "teacher_classes": teacher_classes
    }
    return render(request, 'teacher.html', context)

@login_required(login_url="/login")
def profile(request):
    print("\nTeacher Views: def profile(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    teacher = request.user
    context = {"teacher": teacher}

    return render(request, 'teacher_profile.html', context)

@login_required(login_url="/login")
def deleteTeacherAccount(request):
    print("\nTeacher Views: def deleteTeacherAccount(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    teacher = request.user
    
    if request.method == "POST":
        teacher.delete()
        return redirect("/login")

    context = {"student": teacher}

    return render(request, 'deleteTeacherAccount.html', context)

@login_required(login_url="/login")
def updateTeacherAccount(request):
    print("\nTeacher Views: def updateTeacherAccount(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    teacher = request.user
    form = UpdateAccountForm(instance=teacher)

    if request.method == "POST":
        form = UpdateAccountForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully')
            url = reverse("profile")
            return redirect(url)
            # return redirect("/teacher/profile")

    context = {"form": form, "teacher": teacher}
    return render(request, 'updateTeacherAccount.html', context)

@login_required(login_url="/login")
def teacherClass(request, class_pk):
    print("\nTeacher Views: def teacherClass(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
        
    teacher_class = Class.objects.get(id=class_pk)
    modules = teacher_class.module_set.all()

    students = teacher_class.students.all()

    context = {
        "class_pk": class_pk,
        "teacher_class": teacher_class,
        "modules": modules, 
        "students": students
    }
    return render(request, 'class.html', context)


@login_required(login_url="/login")
def createClass(request):
    print("\nTeacher Views: def createClass(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    form = CreateClassForm()
    if request.method == "POST":
        form = CreateClassForm(request.POST)
        if form.is_valid():
            teacher = request.user

            '''
            teacher_id = request.user.id
            teacher_username = request.user.username
            teacher_password = request.user.password
            '''

            new_class = form.save(commit=False)
            new_class.teacher = teacher
            new_class.save()
            class_pk = new_class.id   

            # create class and redirect
            messages.success(request, 'Class Created successfully')
            url = reverse("teacherClass", kwargs={"class_pk":class_pk})
            return redirect(url)
            # return redirect("/teacher")
    
    context = {"form": form}
    return render(request, 'createClass.html', context)

@login_required(login_url="/login")
def deleteClass(request, class_pk):
    print("\nTeacher Views: def deleteClass(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
        
    teacher_class = Class.objects.get(id=class_pk)
    className = teacher_class.class_name

    if request.method == "POST":
        teacher_class.delete()
        # delete class and redirect
        messages.success(request, f'Successfully deleted class: {className}')
        url = reverse("teacher")
        return redirect(url)
    
    
    context = {"teacher_class": teacher_class}
    return render(request, 'deleteClass.html', context)

@login_required(login_url="/login")
def updateClass(request, class_pk):
    print("\nTeacher Views: def updateclass(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacherClass = Class.objects.get(id=class_pk)
    form = CreateClassForm(instance=teacherClass)

    if request.method == "POST":
        form = CreateClassForm(request.POST, instance=teacherClass)
        if form.is_valid():
            form.save()
            
            # create class and redirect
            messages.success(request, 'Class updated successfully')
            url = reverse("teacherClass", kwargs={"class_pk":class_pk})
            return redirect(url)
        
        

    teacher_class = Class.objects.get(id=class_pk)    
    context = {"form": form, "teacher_class": teacher_class}
    return render(request, 'updateClass.html', context)


@login_required(login_url="/login")
def createModule(request, class_pk):
    print("\nTeacher Views: def createModule(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    form = CreateModuleForm(initial={'parent_class':teacher_class})
    print("Type of request:", request.method)
    if request.method == "POST":
        form = CreateModuleForm(request.POST)
        if form.is_valid():
            print("in is valid")
            teacher = request.user
            module = form.save(commit=False)
            module.teacher = teacher
            module.save() 
            module_pk = module.id        
            # create message and redirect
            messages.success(request, 'Module Created successfully')
            url = reverse("manageModule", kwargs={"class_pk":class_pk, "module_pk": module_pk})
            return redirect(url)
            
    teacher_class = Class.objects.get(id=class_pk)    
    context = {"form": form, "teacher_class": teacher_class}
    return render(request, 'createModule.html', context)


@login_required(login_url="/login")
def deleteModule(request, class_pk, module_pk):
    print("\nTeacher deleteModule: def deleteModule(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    #Get the teacher class 
    teacher_class = Class.objects.get(id=class_pk)
    #Get all the teacher's module 
    teacher_modules = teacher_class.module_set.all()
    print("Teacher's Module: ", teacher_modules)
    #Get the module that matches the module_pk
    print(f"pk: {module_pk}")
    module =  teacher_modules.get(id=module_pk)
    print(" ->", module.id, module.name, module.parent_class)

    if request.method == "POST":
        module.delete()
        
        messages.success(request, 'Module Deleted Successfully')
        url = reverse("modules", kwargs={"class_pk":class_pk})
        return redirect(url)

    context = {
        "class_pk": class_pk,
        "module_pk": module_pk,
        "teacher_class": teacher_class,
        "module": module
    }
    return render(request, 'deleteModule.html', context)


@login_required(login_url="/login")
def updateModule(request, class_pk, module_pk):
    print("\nTeacher Views: def updateModule(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    #Get the teacher class 
    teacher_class = Class.objects.get(id=class_pk)
    #Get all the teacher's module 
    teacher_modules = teacher_class.module_set.all()
    print("Teacher's Module: ", teacher_modules)
    #Get the module that matches the module_pk
    print(f"pk: {module_pk}")
    module =  teacher_modules.get(id=module_pk)
    print(" ->", module.id, module.name, module.parent_class)

    form = CreateModuleForm(instance=module)

    if request.method == "POST":
        form = CreateModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module updated successfully')
            url = reverse("manageModule", kwargs={"class_pk":class_pk, "module_pk": module_pk})
            return redirect(url)

    teacher_class = Class.objects.get(id=class_pk)    
    context = {"form": form,
        "class_pk": class_pk,
        "module_pk": module_pk,
        "teacher_class": teacher_class,
        "module": module,
    }
    
    return render(request, 'updateModule.html', context)


@login_required(login_url="/login")
def updateModuleOrder(request, class_pk, module_pk):
    print("\nTeacher Views: def updateModule(request):\n--------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    #Get the teacher class 
    teacher_class = Class.objects.get(id=class_pk)
    #Get all the teacher's module 
    teacher_modules = teacher_class.module_set.all()
    print("Teacher's Module: ", teacher_modules)
    #Get the module that matches the module_pk
    print(f"pk: {module_pk}")
    module =  teacher_modules.get(id=module_pk)
    print(" ->", module.id, module.name, module.parent_class)

    form = CreateModuleForm(instance=module)

    if request.method == "POST":
        form = CreateModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect("/teacher/class/" + class_pk)
            # messages.success(request, 'Module updated successfully')
            # url = reverse("manageModule", kwargs={"class_pk":class_pk, "module_pk": module_pk})
            # return redirect(url)

    teacher_class = Class.objects.get(id=class_pk)    
    context = {"form": form, "teacher_class": teacher_class}
    return render(request, 'updateModule.html', context)


@login_required(login_url="/login")
def modules(request, class_pk):
    print("\nTeacher Views: def modules(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    teacher_modules = teacher_class.module_set.all()

    if request.method == 'POST':
        orderDict = request.POST.get('orderDict') 
        print("Dictionary of new order: ")
        print("--------------- *** ---------------")
        print("order object: ", orderDict)

        #return HttpResponse(orderDict)
        context = {
            "teacher_class": teacher_class
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
                messages.success(request, 'Module order updated successfully')

            except Module.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Object not found'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No data provided'})

    items = Item.objects.none()
    algorithms = Algorithm.objects.none()
    pages = Page.objects.none()
    empty_modules = Module.objects.none()
    for module in teacher_modules:
        # return all items of this module
        module_items = Item.objects.filter(module=module)
        
        # if items are returned append to the items query set
        if module_items.exists():            
            items = items.union(module_items)
        else: # else, if no items are returned, add the module to the empty_modules queryset
            empty_modules = empty_modules | Module.objects.filter(id=module.id)

    print("All items: ", items)
    print("empty_modules", empty_modules)
    print()
    # create a query set for the pages and algorithms that matches the items in the items queryset
    for item in items:
        item_pages = Page.objects.filter(item=item)
        pages = pages.union(item_pages)
        
        item_algorithms = Algorithm.objects.filter(item=item)
        algorithms = algorithms.union(item_algorithms)


    print("algorithms: ", algorithms)
    for algorithm in algorithms:
        print("algorithm: ", algorithm)
    
    print()
    print("pages: ", pages)
    for page in pages:
        print("page: ", page)
    
    # Order the list of modules and items by order
    teacher_modules = teacher_modules.order_by('order')        
    items = items.order_by('order')
    context = {
        "class_pk": class_pk,
        "teacher_class": teacher_class,
        "modules": teacher_modules,
        "empty_modules": empty_modules,
        "module_number": teacher_modules.count(),
        "items": items,
        "algorithms": algorithms,
        "pages": pages
    }

    return render(request, 'modules.html', context)



@login_required(login_url="/login")
def teacherViewAlgorithm(request, class_pk, algorithm_pk):
    print("\nTeacher Views: def teacherViewAlgorithm(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    algorithm = Algorithm.objects.get(id=algorithm_pk)    
    codes = algorithm.lines.split("\n")
    answers = algorithm.answers.split("\n")
    hints = algorithm.hints.split("\n")

    item = Item.objects.get(id=algorithm.item.id)
    module = Module.objects.get(id=item.module.id)
    module_pk = module.id
    teacher_class = Class.objects.get(id=class_pk)

    

    context = {
        'class_pk': class_pk,
        'module_pk': module_pk,
        'algorithm_pk': algorithm_pk,
        "teacher_class": teacher_class,
        "module": module,
        "algorithm": algorithm,
        "codes": codes,
        "answers": answers,
        "hints": hints,
    }

    return render(request, 'algorithm.html', context)


@login_required(login_url="/login")
def teacherViewPage(request, class_pk, page_pk):
    print("\nTeacher Views: def teacherViewPage(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    page = Page.objects.get(id=page_pk)
    item = Item.objects.get(id=page.item.id)
    module = Module.objects.get(id=item.module.id)
    module_pk = module.id
    teacher_class = Class.objects.get(id=class_pk)

    context = {
        'class_pk': class_pk,
        'module_pk': module_pk,
        'page_pk': page_pk,
        "teacher_class": teacher_class,
        "module": module,
        "page": page
    }

    return render(request, 'page.html', context)



@login_required(login_url="/login")
def updateAlgorithm(request, class_pk, algorithm_pk):
    print("\nTeacher Views: def teacherUpdateAlgorithm(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    algorithm = Algorithm.objects.get(id=algorithm_pk) 
    item = Item.objects.get(id=algorithm.item.id)
    module = Module.objects.get(id=item.module.id)
    module_pk = module.id
    teacher_class = Class.objects.get(id=class_pk)

    if request.method == "POST" and request.POST.getlist('submitAlgorithmForm'):
        print(f"POST = {request.POST}")
        table = request.POST.getlist('table_data')
        print("TABLE = ", table)

        formattedTable = []
        for item in table:
            formattedItem = eval(item)
            formattedTable.append(formattedItem)
        formattedTable = formattedTable[0]
        print("FORMATTED_TABLE = ", formattedTable)

        lines = ""
        answers = ""
        hints = ""

        for i in range(len(formattedTable)):
            print("Line: ", formattedTable[i])
            lines += formattedTable[i]["code"] + "\n"
            
            answer = formattedTable[i]["answer"]
            answer = clean_answer(answer)
            answers += answer + "\n"

            hint = formattedTable[i]["hint"]
            # strip the hint from spaces 
            hint = hint.rstrip()
            # add one space after the hint. Needed to ensure at least an empty hint is saved for each line
            # Needed for zip as zip needs all its list to have the save number of lines
            hint += " "
            
            hints += hint + "\n"
        
        print(f"\n\nLines:\n{lines}")
        print(f"Answers:\n{answers}")
        print(f"Hints:\n{hints}]")

        algorithmName = request.POST.getlist('algorithm_name')[0]
        form = AlgorithmForm
        # return HttpResponse(
        #     "Name: " + algorithmName + "\n"
        #     "Lines\n" + 
        #     lines + 
            
        #     "\nAnswers\n" +
        #      answers + 
        #     "\nHints\n" + 
        #      hints
        #  )
            
        algorithm.name = algorithmName
        algorithm.lines = lines.rstrip("\n")
        algorithm.answers = answers.rstrip("\n")
        algorithm.hints = hints.rstrip("\n")
        algorithm.save()
        messages.success(request, 'Algorithm updated successfully')

        url = reverse("teacherViewAlgorithm", kwargs={"class_pk": class_pk, "algorithm_pk": algorithm_pk})
        return redirect(url)
    

    codes = algorithm.lines.split("\n")
    answers = algorithm.answers.split("\n")
    hints = algorithm.hints.split("\n")
    data = zip(codes, answers, hints)
    
    context = {
        'class_pk': class_pk,
        'module_pk': module_pk,
        'algorithm_pk': algorithm_pk,
        "teacher_class": teacher_class,
        "module": module,
        "algorithm": algorithm,
        "codes": codes,
        "answers": answers,
        "hints": hints,
        "data": data
    }
    return render(request, 'updateAlgorithm.html', context)

@login_required(login_url="/login")
def updatePage(request, class_pk, page_pk):
    print("\nTeacher Views: def teacherUpdatePage(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    page = Page.objects.get(id=page_pk)
    item = Item.objects.get(id=page.item.id)
    module = Module.objects.get(id=item.module.id)
    module_pk = module.id
    teacher_class = Class.objects.get(id=class_pk)

    form = CreatePageForm(instance=page, initial={'item': item})
    if request.method == 'POST':
        form = CreatePageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            
            # create message and redirect
            messages.success(request, 'Page Updated Successfully')
            url = reverse("teacherViewPage", kwargs={"class_pk": class_pk, "page_pk": page_pk})
            return redirect(url)


    context = {
        'class_pk': class_pk,
        'module_pk': module_pk,
        'page_pk': page_pk,
        "teacher_class": teacher_class,
        "module": module,
        "page": page,
        "form":form
    }

    return render(request, 'updatePage.html', context)


@login_required(login_url="/login")
def deletePage(request, class_pk, page_pk):
    print("\nTeacher Views: def deletePage(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    page = Page.objects.get(id=page_pk)
    item = Item.objects.get(id=page.item.id)
    module =  Module.objects.get(id=item.module.id)
    module_pk = module.id
    teacher_class = Class.objects.get(id=class_pk)

    print(f"\n{item}\n{page}")

    if request.method == "POST":
        item.delete()

        # create message and redirect
        messages.success(request, 'Page Deleted successfully')
        url = reverse("manageModule", kwargs={"class_pk": class_pk, "module_pk": module_pk})
        return redirect(url)
    
    context = {
    "class_pk": class_pk,
    "module_pk": module_pk,
    "page_pk": page_pk,
    "teacher_class": teacher_class,
    "module": module,
    "page": page
    }
    return render(request, 'deletePage.html', context)

@login_required(login_url="/login")
def deleteAlgorithm(request, class_pk, algorithm_pk):
    print("\nTeacher Views: def deleteAlgorithm(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    algorithm = Algorithm.objects.get(id=algorithm_pk)
    item = Item.objects.get(id=algorithm.item.id)
    module =  Module.objects.get(id=item.module.id)
    module_pk = module.id
    teacher_class = Class.objects.get(id=class_pk)

    if request.method == "POST":        
        algorithmName = algorithm.name
        item.delete()
        # create message and redirect
        messages.success(request, f'Successfully deleted algorithm: {algorithmName}')
        url = reverse("manageModule", kwargs={"class_pk": class_pk, "module_pk": module_pk})
        return redirect(url)
    
    
    context = {
    "class_pk": class_pk,
    "module_pk": module_pk,
    "algorithm_pk":algorithm_pk,
    "teacher_class": teacher_class,
    "module": module,
    "algorithm":algorithm
    }
    return render(request, 'deleteAlgorithm.html', context)


@login_required(login_url="/login")
def deleteModule_template(request, class_pk, module_pk):
    print("\nTeacher deleteModule: def deleteModule(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    #Get the teacher class 
    teacher_class = Class.objects.get(id=class_pk)
    #Get all the teacher's module 
    teacher_modules = teacher_class.module_set.all()
    print("Teacher's Module: ", teacher_modules)
    #Get the module that matches the module_pk
    print(f"pk: {module_pk}")
    module =  teacher_modules.get(id=module_pk)
    print(" ->", module.id, module.name, module.parent_class)

    if request.method == "POST":
        module.delete()
        url = reverse("teacherClass", kwargs={"class_pk":teacher_class.id})
        return redirect(url)

    context = {"teacher_class": teacher_class, "module": module}
    return render(request, 'deleteModule.html', context)



@login_required(login_url="/login")
def manageModule(request, class_pk, module_pk):
    print("\nTeacher Views: def module(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    
    algorithms = Algorithm.objects.none()
    pages = Page.objects.none()

    if request.method == 'POST':

        orderDict = request.POST.get('orderDict') 
        print("Dictionary of new order: ")
        print("--------------- *** ---------------")
        print("order object: ", orderDict)

        # return HttpResponse(orderDict)
        context = {
            "teacher_class": teacher_class
        }
        
        if orderDict:
            try:
                # Convert string representation to dictionary
                orderDict = json.loads(orderDict)  
                # Parse the order dictionary and update every module that matches the obj_id
                for obj_id, new_order in orderDict.items():  
                    obj = Item.objects.get(pk=obj_id)
                    obj.order = new_order
                    obj.save()
                
                messages.success(request, 'Algorithm/Page order updated successfully')
            
            except Module.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Object not found'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No data provided'})


    items = Item.objects.filter(module=module.id)
    for item in items:
        item_pages = Page.objects.filter(item=item)
        pages = pages.union(item_pages)
        
        item_algorithms = Algorithm.objects.filter(item=item)
        algorithms = algorithms.union(item_algorithms)

    print()
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

    items = items.order_by('order')
    context = {
        "class_pk": class_pk,
        "module_pk": module_pk,
        "teacher_class": teacher_class,
        "module": module,
        "items": items,
        "algorithms": algorithms,
        "pages": pages
    }
    return render(request, 'manageModule.html', context)



@login_required(login_url="/login")
def createAlgorithm(request, class_pk, module_pk):
    print("\ncreateAlgorithm Views: def createAlgorithm(request):\n-------------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    context = {"teacher_class": teacher_class, "module": module}

    # for table code line validation
    invalidCodeLine = False

    # variables for extracting table data from the HTML form
    lines = []
    answers = []
    hints = []

    if request.method == "POST" and request.POST.getlist('fileUploadForm'):
        print("fileUpload")
        try:
            algorithm_file = request.FILES['algorithmUpload']
            algorithm_file_name = algorithm_file.name
            algorithm_file_size = algorithm_file.size
            algorithm_file_content_type = algorithm_file.content_type
            algorithm_file_lines = algorithm_file.open().readlines()
            algorithm_file.close()

            algorithm_file_lines = [line.decode("utf-8") for line in algorithm_file_lines]

            answerkey_file = request.FILES['answerkeyUpload']
            answerkey_file_name = answerkey_file.name
            answerkey_file_size = answerkey_file.size
            answerkey_file_content_type = answerkey_file.content_type
            answerkey_file_lines = answerkey_file.open().readlines()
            answerkey_file.close()

            # Debugging Messages:
            print("Name of algorithm file: ", algorithm_file_name)
            print("Size of algorithm file: ", algorithm_file_size)
            
            algorithm_line_count = sum(1 for line in algorithm_file_lines)        
            print("number of line ", algorithm_line_count)

            print("Content Type of algorithm file: ", algorithm_file_content_type)
            print("Was the algorithm file closed? ", algorithm_file.closed)

            print("Name of answerkey file: ", answerkey_file_name)
            print("Size of answerkey file: ", answerkey_file_size)        
            answerkey_line_count = sum(1 for line in answerkey_file_lines)        
            print("number of line ", answerkey_line_count)
            print("Content Type of answerkey file: ", answerkey_file_content_type)
            print("Was the answerkey file closed? ", answerkey_file.closed)

            algorithm = zip(algorithm_file_lines, answerkey_file_lines)
            print(f"algorithm_file_lines: {algorithm_file_lines}")

            for code, answer in algorithm:
                print(f"code: {len(code)} - answer: {len(answer.decode())}")

                if len(code) == 1 and len(answer.decode()) != 1:
                    invalidCodeLine = True
                    print("Missing code")
                elif len(code) != 1 and len(answer.decode()) == 1:
                    invalidCodeLine = True
                    print("Missing answer")
            
            context.update({
                "algorithm_file_lines": algorithm_file_lines,
                "algorithm_line_count": algorithm_line_count,
                "answerkey_file_lines": answerkey_file_lines,
                "answerkey_line_count": answerkey_line_count,
                "algorithm": algorithm,
                "invalidCodeLine": invalidCodeLine,
            })

            if request.method == "POST":
                print(request.POST)

        except MultiValueDictKeyError:
            print("No file was chosen.")

    elif request.method == "POST" and request.POST.getlist('submitAlgorithmForm'):
        print(f"POST = {request.POST}")
        table = request.POST.getlist('table_data')
        print("TABLE = ", table)

        formattedTable = []
        for item in table:
            formattedItem = eval(item)
            formattedTable.append(formattedItem)
        formattedTable = formattedTable[0]
        print("FORMATTED_TABLE = ", formattedTable)

        lines = ""
        answers = ""
        hints = ""

        for i in range(len(formattedTable)):
            print("Line: ", formattedTable[i])
            lines += formattedTable[i]["code"] + "\n"
            
            answer = formattedTable[i]["answer"]
            answer = clean_answer(answer)
            answers += answer + "\n"

            hint = formattedTable[i]["hint"]             
            # strip the hint from spaces 
            hint = hint.rstrip()
            # add one space after the hint. Needed to ensure at least an empty hint is saved for each line
            # Needed for zip as zip needs all its list to have the save number of lines
            hint += " "

            hints += hint + "\n"
        
        print(f"\n\nLines:\n{lines}")
        print(f"Answers:\n{answers}")
        print(f"Hints:\n{hints}]")

        # return HttpResponse(
        #     "Lines\n" + 
        #     lines + 
            
        #     "\nAnswers\n" +
        #      answers + 
        #     "\nHints\n" + 
        #      hints
        #  )

        # After the posted data for the algorithm are validated
        # Create an Item for this algorithm
        item = Item.objects.create(
            type = ItemType.objects.get(type="Algorithm"),
            module = Module.objects.get(id=module_pk),
        )

        algorithmName = request.POST.getlist('algorithm_name')[0]

        algorithm = Algorithm.objects.create(
            name = algorithmName,
            item = item,
            lines = lines.rstrip("\n"),
            answers = answers.rstrip("\n"),
            hints = hints.rstrip("\n"),
        )
        messages.success(request, 'Algorithm created successfully')

        url = reverse("teacherViewAlgorithm", kwargs={"class_pk": class_pk, "algorithm_pk": algorithm.id})
        return redirect(url)
    
    return render(request, 'createAlgorithm.html', context)


@login_required(login_url="/login")
def createAlgorithm2(request, class_pk, module_pk):
    print("\ncreateAlgorithm2 Views: def createAlgorithm2(request):\n-------------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    context = {"teacher_class": teacher_class, "module": module}

    # for table code line validation
    invalidCodeLine = False

    # variables for extracting table data from the HTML form
    lines = []
    answers = []
    hints = []

    if request.method == "POST" and request.POST.getlist('fileUploadForm'):
        print("fileUpload")
        try:
            algorithm_file = request.FILES['algorithmUpload']
            algorithm_file_name = algorithm_file.name
            algorithm_file_size = algorithm_file.size
            algorithm_file_content_type = algorithm_file.content_type
            algorithm_file_lines = algorithm_file.open().readlines()
            algorithm_file.close()

            algorithm_file_lines = [line.decode("utf-8") for line in algorithm_file_lines]

            # Debugging Messages:
            print("Name of algorithm file: ", algorithm_file_name)
            print("Size of algorithm file: ", algorithm_file_size)
            
            algorithm_line_count = sum(1 for line in algorithm_file_lines)        
            print("number of line ", algorithm_line_count)

            print("Content Type of algorithm file: ", algorithm_file_content_type)
            print("Was the algorithm file closed? ", algorithm_file.closed)

            algorithm = zip(algorithm_file_lines)
            print(f"algorithm_file_lines: {algorithm_file_lines}")

            answerkey_lines = []

            # Prefill the answers for every line of code
            for code in algorithm_file_lines:
                print(f"code: {code}")

                split_line = code.strip().split(' ')
                print(f"split_code: {split_line}")

                # If blank line, no answer
                if len(code.strip()) == 0 or split_line[0][0] == "#":
                    answerkey_lines.append("")
                
                # If not blank line
                else:
                    split_line = code.strip().split(' ')
                    print(f"split_code: {split_line}")

                    # If loop, set answer to O(n)
                    if split_line[0] == "for" or split_line[0] == "while":
                        answerkey_lines.append("O(n)")
                    
                    # Otherwise, set answer to O(1)
                    else:
                        answerkey_lines.append("O(1)")

            print(f"answerkey_lines: {answerkey_lines}")

            for answer in answerkey_lines:
                print(f"answer: {answer}")
            
            context.update({
                "algorithm_file_lines": algorithm_file_lines,
                "algorithm_line_count": algorithm_line_count,
                "answerkey_lines": answerkey_lines,
                "algorithm": algorithm,
                "invalidCodeLine": invalidCodeLine,
            })

            if request.method == "POST":
                print(request.POST)

        except MultiValueDictKeyError:
            print("No file was chosen.")

    elif request.method == "POST" and request.POST.getlist('submitAlgorithmForm'):
        print(f"POST = {request.POST}")
        table = request.POST.getlist('table_data')
        print("TABLE = ", table)

        formattedTable = []
        for item in table:
            formattedItem = eval(item)
            formattedTable.append(formattedItem)
        formattedTable = formattedTable[0]
        print("FORMATTED_TABLE = ", formattedTable)

        lines = ""
        answers = ""
        hints = ""

        for i in range(len(formattedTable)):
            print("Line: ", formattedTable[i])
            lines += formattedTable[i]["code"] + "\n"
            
            answer = formattedTable[i]["answer"]
            answer = clean_answer(answer)
            answers += answer + "\n"

            hint = formattedTable[i]["hint"]             
            # strip the hint from spaces 
            hint = hint.rstrip()
            # add one space after the hint. Needed to ensure at least an empty hint is saved for each line
            # Needed for zip as zip needs all its list to have the save number of lines
            hint += " "

            hints += hint + "\n"
        
        print(f"\n\nLines:\n{lines}")
        print(f"Answers:\n{answers}")
        print(f"Hints:\n{hints}]")

        # return HttpResponse(
        #     "Lines\n" + 
        #     lines + 
            
        #     "\nAnswers\n" +
        #      answers + 
        #     "\nHints\n" + 
        #      hints
        #  )

        # After the posted data for the algorithm are validated
        # Create an Item for this algorithm
        item = Item.objects.create(
            type = ItemType.objects.get(type="Algorithm"),
            module = Module.objects.get(id=module_pk),
        )

        algorithmName = request.POST.getlist('algorithm_name')[0]

        algorithm = Algorithm.objects.create(
            name = algorithmName,
            item = item,
            lines = lines.rstrip("\n"),
            answers = answers.rstrip("\n"),
            hints = hints.rstrip("\n"),
        )
        messages.success(request, 'Algorithm created successfully')

        url = reverse("teacherViewAlgorithm", kwargs={"class_pk": class_pk, "algorithm_pk": algorithm.id})
        return redirect(url)
    
    return render(request, 'createAlgorithm2.html', context)


@login_required(login_url="/login")
def createPage(request, class_pk, module_pk):
    print("\ncreatePage Views: def createPage(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)    
    form = CreatePageForm()
    context = {"form": form, "teacher_class": teacher_class, "module": module}

    if request.method == "POST":
        # Get the posted element
        name = request.POST.get('name')
        content = request.POST.get('content')
        
        # Create an Item for this page
        item = Item.objects.create(
            type = ItemType.objects.get(type="Page"),
            module = Module.objects.get(id=module_pk),
        )
        page = Page.objects.create(
            name = name,
            item = item,
            content = content,
        )
        page_pk = page.id

        # create message and redirect
        messages.success(request, 'Page Created successfully')
        url = reverse("teacherViewPage", kwargs={"class_pk": class_pk, "page_pk": page_pk})
        return redirect(url)
    
    return render(request, 'createPage.html', context)