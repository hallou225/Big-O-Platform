from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bigo.forms import *
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

'''
@login_required(login_url="/login")
def teacher(request):
    print("Teacher Function")
    checkTeacherRole(request)
    teacher_id = request.user.id
    teacher_username = request.user.username
    teacher_password = request.user.password
    teacher_display_name = request.user.display_name

    teacher_classes = Class.objects.filter(teacher_id=teacher_id)

    context = {"teacher_id": teacher_id, "teacher_username": teacher_username, "teacher_password": teacher_password, "teacher_display_name": teacher_display_name, "teacher_classes": teacher_classes}
    return render(request, 'teacher.html', context)
'''

print("Start")
def isTeacher(request):
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

    teacher_classes = Class.objects.filter(teacher_id=teacher_id)

    context = {"teacher_id": teacher_id, "teacher_username": teacher_username, "teacher_password": teacher_password, "teacher_display_name": teacher_display_name, "teacher_classes": teacher_classes}
    return render(request, 'teacher.html', context)

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

@login_required(login_url="/login")
def profile(request):
    print("Teacher Views: def profile(request):")
    if not isTeacher(request):
        return redirect("/login")
    
    teacher = request.user
    context = {"teacher": teacher}

    return render(request, 'profile.html', context)

@login_required(login_url="/login")
def teacherClass(request, class_pk):
    print("Teacher Views: def teacherClass(request):")
    if not isTeacher(request):
        return redirect("/login")
        
    teacher_class = Class.objects.get(id=class_pk)

    class_name = teacher_class.class_name
    modules = teacher_class.module_set.all()

    context = {"teacher_class": teacher_class, "modules": modules}
    return render(request, 'class.html', context)

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

    context = {"form": form}
    return render(request, 'updateClass.html', context)

@login_required(login_url="/login")
def module(request, class_pk, module_pk):
    print("Teacher Views: def module(request):")
    if not isTeacher(request):
        return redirect("/login")

    teacherClass = Class.objects.get(id=class_pk)
    module = Module.objects.get(id=module_pk)
    context = {"teacherClass": teacherClass, "module": module}

    try:
        algorithm_file = request.FILES['algorithmUpload']
        algorithm_file_name = algorithm_file.name
        algorithm_file_size = algorithm_file.size
        algorithm_file_content_type = algorithm_file.content_type
        algorithm_file_lines = algorithm_file.open().readlines()
        algorithm_file.close()

        answerkey_file = request.FILES['answerkeyUpload']
        answerkey_file_name = answerkey_file.name
        answerkey_file_size = answerkey_file.size
        answerkey_file_content_type = answerkey_file.content_type
        answerkey_file_lines = answerkey_file.open().readlines()
        answerkey_file.close()

        # Debugging Messages:
        print("Name of algorithm file: ", algorithm_file_name)
        print("Size of algorithm file: ", algorithm_file_size)
        print("Content Type of algorithm file: ", algorithm_file_content_type)
        print("Was the algorithm file closed? ", algorithm_file.closed)

        print("Name of answerkey file: ", answerkey_file_name)
        print("Size of answerkey file: ", answerkey_file_size)
        print("Content Type of answerkey file: ", answerkey_file_content_type)
        print("Was the answerkey file closed? ", answerkey_file.closed)

        '''
        context.update({"file": file, "file_name": file_name,
        "file_size": file_size, "file_content_type": file_content_type,
        "file_lines": file_lines})
        '''
        context.update({"algorithm_file_lines": algorithm_file_lines,
        "answerkey_file_lines": answerkey_file_lines})

    except MultiValueDictKeyError:
        print("No file was chosen.")

    return render(request, 'module.html', context)
