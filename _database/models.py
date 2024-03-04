from django.db import models

# Create your models here.

class Student(models.Model):
    firstname    = models.CharField(max_length=100, null=True)
    lastname     = models.CharField(max_length=100, null=True)
    email        = models.EmailField(max_length=100, null=True)
    password     = models.CharField(max_length=50, null=True)
    role         = models.CharField(max_length=10, choices=[("S", "Student"), ("T", "Teacher")], default=("S", "Student"))

    class1        = models.CharField(max_length=100, null=True)
    class2        = models.CharField(max_length=100, null=True)
    class3        = models.CharField(max_length=100, null=True)

    classes = [class1, class2, class3]

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    #ArrayField(models.CharField(max_length=255))
    

    def __str__(self) -> str:
        return self.firstname + " " + self.lastname


class Teacher(models.Model):
    firstname    = models.CharField(max_length=100, null=True)
    lastname     = models.CharField(max_length=100, null=True)
    email        = models.EmailField(max_length=100, null=True)
    password     = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self) -> str:
        return self.firstname + " " + self.lastname


class Class(models.Model):
    code    = models.CharField(max_length=100, null=True)
    className     = models.CharField(max_length=100, null=True)
    teacherName        = models.EmailField(max_length=100, null=True)
    password     = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    student1        = models.CharField(max_length=100, null=True)
    student2        = models.CharField(max_length=100, null=True)
    student3        = models.CharField(max_length=100, null=True)

    students = [student1, student2, student3]
    
    module1        = models.CharField(max_length=100, null=True)
    module2        = models.CharField(max_length=100, null=True)
    module3        = models.CharField(max_length=100, null=True)

    modules = [module1, module2, module3]
    

    def __str__(self) -> str:
        return self.firstname + " " + self.lastname


class Module(models.Model):
    moduleName    = models.CharField(max_length=100, null=True)
    numberOfTasks     = models.CharField(max_length=100, null=True)

    task1        = models.CharField(max_length=100, null=True)
    task2        = models.CharField(max_length=100, null=True)
    task3        = models.CharField(max_length=100, null=True)

    tasks = [task1, task2, task3]


    def __str__(self) -> str:
        return self.firstname + " " + self.lastname


class Task(models.Model):
    taskName    = models.CharField(max_length=100, null=True)
    taskType     = models.CharField(max_length=100, null=True)
    email        = models.EmailField(max_length=100, null=True)
    password     = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    acceptedAnswer1        = models.CharField(max_length=100, null=True)
    acceptedAnswer2        = models.CharField(max_length=100, null=True)
    acceptedAnswer3        = models.CharField(max_length=100, null=True)

    acceptedAnswers = [acceptedAnswer1, acceptedAnswer2, acceptedAnswer3]


    def __str__(self) -> str:
        return self.firstname + " " + self.lastname
