from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse

# Create your views here.
def isTeacher(request):
    """! The isTeacher class.
    Checks the role of the user trying to access a page
    """
    print("checkRole function")
    if request.user.is_authenticated:
        print("request.user.role: ", str(request.user.role))
        if str(request.user.role) == "Teacher":
            return True
        else:
            print("redirect to /login")
            return False

@login_required(login_url="/login")
def teacher(request):
    print("Teacher Views: def teacher(request):")
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
    print("Teacher Views: def profile(request):")
    if not isTeacher(request):
        return redirect("/login")
    
    teacher = request.user
    context = {"teacher": teacher}

    return render(request, 'teacher_profile.html', context)

@login_required(login_url="/login")
def deleteTeacherAccount(request):
    print("Teacher Views: def deleteTeacherAccount(request):")
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
    print("Teacher Views: def updateTeacherAccount(request):")
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
    print("Teacher Views: def teacherClass(request):")
    if not isTeacher(request):
        return redirect("/login")
        
    teacher_class = Class.objects.get(id=class_pk)
    modules = teacher_class.module_set.all()

    students = teacher_class.students.all()

    context = {"teacher_class": teacher_class, "modules": modules, "students": students}
    return render(request, 'class.html', context)


@login_required(login_url="/login")
def createclass(request):
    print("Teacher Views: def createclass(request):")
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
    return render(request, 'createclass.html', context)

def deleteClass(request, class_pk):
    print("Teacher Views: def deleteClass(request):")
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
    print("Teacher Views: def updateclass(request):")
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
    print("Teacher Views: def createModule(request):")
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
def module(request, class_pk, module_pk):
    print("Teacher Views: def module(request):")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)

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
    
    for algorithm_name, lines in algorithm_lines.items():
        #print(f"Algorithm: {algorithm_name}")
        output = f"""
                <p>{algorithm_name}</p>
                 """
        for line in lines:
            #print("Code: ", {line["code"]})
            #print("Answer: ", {line["answer"]})
            #print("Hint: ", {line["hint"]})

            output += f"""
                <p>{line["code"]}</p>
                <p>{line["answer"]}</p>
                <p>{line["hint"]}</p>
                 """
                
            print(output)
    
    context = {"teacher_class": teacher_class, "module": module, "algorithm_lines_items": algorithm_lines.items()}

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

        '''
        context.update({"file": file, "file_name": file_name,
        "file_size": file_size, "file_content_type": file_content_type,
        "file_lines": file_lines})
        '''
        
        algorithm = zip(algorithm_file_lines, answerkey_file_lines)
        
        context.update({
            "algorithm_file_lines": algorithm_file_lines,
            "algorithm_line_count": algorithm_line_count,
            "answerkey_file_lines": answerkey_file_lines,
            "answerkey_line_count": answerkey_line_count,
            "algorithm": algorithm
        })

    except MultiValueDictKeyError:
        print("No file was chosen.")

    return render(request, 'module.html', context)



@login_required(login_url="/login")
def createAlgorithm(request, class_pk, module_pk):
    print("createAlgorithm Views: def createAlgorithm(request):")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    context = {"teacher_class": teacher_class, "module": module}

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

        '''
        context.update({"file": file, "file_name": file_name,
        "file_size": file_size, "file_content_type": file_content_type,
        "file_lines": file_lines})
        '''
        
        algorithm = zip(algorithm_file_lines, answerkey_file_lines)
        
        context.update({
            "algorithm_file_lines": algorithm_file_lines,
            "algorithm_line_count": algorithm_line_count,
            "answerkey_file_lines": answerkey_file_lines,
            "answerkey_line_count": answerkey_line_count,
            "algorithm": algorithm
        })

    except MultiValueDictKeyError:
        print("No file was chosen.")

    return render(request, 'createAlgorithm.html', context)

@login_required(login_url="/login")
def createPage(request, class_pk, module_pk):
    print("createPage Views: def createPage(request):")
    if not isTeacher(request):
        return redirect("/login")

    teacher_class = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    context = {"teacher_class": teacher_class, "module": module}

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

        '''
        context.update({"file": file, "file_name": file_name,
        "file_size": file_size, "file_content_type": file_content_type,
        "file_lines": file_lines})
        '''
        
        algorithm = zip(algorithm_file_lines, answerkey_file_lines)
        
        context.update({
            "algorithm_file_lines": algorithm_file_lines,
            "algorithm_line_count": algorithm_line_count,
            "answerkey_file_lines": answerkey_file_lines,
            "answerkey_line_count": answerkey_line_count,
            "algorithm": algorithm
        })

    except MultiValueDictKeyError:
        print("No file was chosen.")

    return render(request, 'createPage.html', context)


@login_required(login_url="/login")
def algorithm(request, class_pk, module_pk):
    print("upload Algorithm Views: def uploadAlgorithm(request):")
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
