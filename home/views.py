from urllib.request import Request
from django.shortcuts import render, HttpResponse
from _database.models import *

# Create your views here.

def home(request):
    '''
    students = Student.objects.all()
    teachers = Teacher.objects.all()

    #students_usernames_and_passwords = list(students.values('username', 'password'))
    student_data = list(students.values("username", "password"))
    teacher_data = list(teachers.values("username", "password"))

    total_students = students.count()
    total_teachers = teachers.count()

    context = {
        "students": students,
        "teachers": teachers,
        "total_students": total_students,
        "total_teachers": total_teachers
        }

    return render(request, 'home.html', context)
    '''
    return render(request, 'home.html')

def teacher(request):
    return render(request, 'teacher.html')

def signup(request):
    return render(request, 'signup.html')
