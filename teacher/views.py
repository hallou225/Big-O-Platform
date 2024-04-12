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
            return redirect("/teacher/profile")
 
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

    context = {"teacher_class": teacher_class, "modules": modules, "students": students}
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

            return redirect("/teacher")
    
    context = {"form": form}
    return render(request, 'createClass.html', context)


@login_required(login_url="/login")
def deleteClass(request, class_pk):
    print("\nTeacher Views: def deleteClass(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")
        
    teacher_class = Class.objects.get(id=class_pk)

    if request.method == "POST":
        teacher_class.delete()
        return redirect("/teacher")

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
            return redirect("/teacher/class/" + class_pk)

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
            new_class = form.save(commit=False)
            new_class.teacher = teacher
            new_class.save()            
            url = reverse("teacherClass", kwargs={"class_pk":teacher_class.id})
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
        url = reverse("teacherClass", kwargs={"class_pk":teacher_class.id})
        return redirect(url)

    context = {"teacher_class": teacher_class, "module": module}
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
            return redirect("/teacher/class/" + class_pk)

    teacher_class = Class.objects.get(id=class_pk)    
    context = {"form": form, "teacher_class": teacher_class}
    return render(request, 'updateModule.html', context)

@login_required(login_url="/login")
def modules(request, class_pk):
    print("\nTeacher Views: def module(request):\n------------------- modules ----------------------------")
    if not isTeacher(request):
        return redirect("/login")


    
    teacher_class = Class.objects.get(id=class_pk)
    teacher_modules = teacher_class.module_set.all()

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
    
    

    # for module in teacher_modules:
    #     print("module.name: ", module.name)
    #     for item in items:
    #         if module.name == item.module.name:
    #             print("Type: ", item.type)
    #             if str(item.type) == "Algorithm":
    #                 #i = Algorithm.objects.get(item=item.module.id)                 
    #                 i = Algorithm.objects.filter(item=item.id)
    #                 A.append(i)
    #                 print(i)
    #                 print("this is an algorithm\n")     

    #             elif str(item.type) == "Page":     
    #                 i = Page.objects.get(item=item.id)
    #                 P.append(i)
    #                 print(i)
    #                 print("this is a page: \n")          
                
    #             print("Algorithms ", A)
    #             print("Pages: ", P)
            

    # teacher_class = Class.objects.get(id=class_pk)
    # module = Module.objects.get(id=module_pk)

    # algorithm_lines = {}
    # for item in module.item_set.all():
    #     if item.type == "Algorithm":
    #         if algorithm.name not in algorithm_lines:
    #             algorithm_lines[algorithm.name] = []
    #         for line in algorithm.line_set.all():
    #             algorithm_lines[algorithm.name].append({
    #             'code': line.code,
    #             'answer': line.answer,
    #             'hint': line.hint
    #         })
    # for algorithm_name, lines in algorithm_lines.items():
    #     #print(f"Algorithm: {algorithm_name}")
    #     output = f"""
    #             <p>{algorithm_name}</p>
    #              """
    #     for line in lines:
    #         output += f"""
    #             <p>{line["code"]}</p>
    #             <p>{line["answer"]}</p>
    #             <p>{line["hint"]}</p>
    #              """
                
    #         print(output)
    #     if item.type == "Pages":
    #         print("page:", item.name)
        

    context = {
        "teacher_class": teacher_class,
        "modules": teacher_modules,
        "empty_modules": empty_modules,
        "module_number": teacher_modules.count(),
        "items": items,
        "algorithms": algorithms,
        "pages": pages
    }
    
    # context = {"teacher_class": teacher_class, "module": module, "algorithm_lines_items": algorithm_lines.items()}

    return render(request, 'modules.html', context)



@login_required(login_url="/login")
def teacherViewAlgorithm(request, class_pk, algorithm_pk):
    print("\nTeacher Views: def module(request):\n------------------------ teacherViewAlgorithm -----------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    return render(request, '_template.html')

@login_required(login_url="/login")
def teacherViewPage(request, class_pk, page_pk):
    print("\nTeacher Views: def module(request):\n------------------------ teacherViewPage -----------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    return render(request, '_template.html')

@login_required(login_url="/login")
def deletePage(request, class_pk, module_pk, page_pk):
    print("\nTeacher Views: def deletePage(request):\n------------------------ deletePage -----------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    context = {
    "class_pk": class_pk,
    "module_pk": module_pk,
    "page_pk": page_pk
    }
    return render(request, 'deletePage.html', context)

@login_required(login_url="/login")
def deleteAlgorithm(request, class_pk, module_pk, algorithm_pk):
    print("\nTeacher Views: def deleteAlgorithm(request):\n------------------------ deleteAlgorithm -----------------------")
    if not isTeacher(request):
        return redirect("/login")
    
    context = {
    "class_pk": class_pk,
    "module_pk": module_pk,
    "algorithm_pk":algorithm_pk
    }
    return render(request, 'deleteAlgorithm.html', context)








@login_required(login_url="/login")
def module(request, class_pk, module_pk):
    print("\nTeacher Views: def module(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")


    
    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    items = Item.objects.filter(module=module.id)

    algorithms = Algorithm.objects.none()
    pages = Page.objects.none()

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

    context = {
        
        "teacher_class": teacher_class,
        "module": module,
        "items": items,
        "algorithms": algorithms,
        "pages": pages
    }
    
    # context = {"teacher_class": teacher_class, "module": module, "algorithm_lines_items": algorithm_lines.items()}

    return render(request, 'module.html', context)



@login_required(login_url="/login")
def createAlgorithm(request, class_pk, module_pk):
    print("\ncreateAlgorithm Views: def createAlgorithm(request):\n------------------- current ----------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    context = {"teacher_class": teacher_class, "module": module}

    invalidCodeLine = False

    # Extracting table data from the HTML form
    lines = []
    answers = []
    hints = []
        
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
            answers += formattedTable[i]["answer"] + "\n"
            hints += formattedTable[i]["hint"] + "\n"
        
        print(f"Lines:\n{lines}")
        print(f"Answers:\n{answers}")
        print(f"Hints:\n{hints}]")

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
    
    elif request.method == "POST" and request.POST.getlist('fileUploadForm'):
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

    return render(request, 'createAlgorithm.html', context)



@login_required(login_url="/login")
def createPage(request, class_pk, module_pk):
    print("\ncreatePage Views: def createPage(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    context = {"teacher_class": teacher_class, "module": module}

    return render(request, 'createPage.html', context)


@login_required(login_url="/login")
def algorithm(request, class_pk, module_pk):
    print("\nupload Algorithm Views: def uploadAlgorithm(request):\n-----------------------------------------------")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    form = AlgorithmForm()


    context = {
        "form":form,
        "teacher_class": teacher_class,
        "module": module
    }
    return render(request, 'algorithm.html', context)
