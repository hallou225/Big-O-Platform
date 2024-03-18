from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
    first_name      = models.CharField(max_length=100, null=True)        # Required Field
    middle_name     = models.CharField(max_length=100, null=True)       # Optional Field
    last_name       = models.CharField(max_length=100, null=True)         # Required Field
    display_name    = models.CharField(max_length=100, null=True)      # Optional Field
    username        = models.CharField(max_length=100, null=True)          # Required Field
    password        = models.CharField(max_length=100, null=True)          # Required Field
    email           = models.CharField(max_length=100, null=True)             # Required Field
    date_created    = models.DateTimeField(auto_now_add=True)          # No Specification Required

    def __str__(self):
        return self.first_name + " " + self.last_name
    

class Student(models.Model):
    first_name   = models.CharField(max_length=100, null=True)         # Required Field
    middle_name  = models.CharField(max_length=100, null=True)        # Optional Field
    last_name    = models.CharField(max_length=100, null=True)          # Required Field
    username     = models.CharField(max_length=100, null=True)           # Required Field
    password     = models.CharField(max_length=100, null=True)           # Required Field
    email        = models.CharField(max_length=100, null=True)              # Required Field
    date_created = models.DateTimeField(auto_now_add=True)           # No Specification Required

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class Language(models.Model):
    name = models.CharField(max_length=100)                          # Required Field

    def __str__(self) -> str:
        return self.name 
    

class Module(models.Model):
    name = models.CharField(max_length=100)                          # Required Field
    # number_of_question
    # algorithm_id
    def __str__(self) -> str:
        return self.name
    
class Year(models.Model):                      
    start_date    = models.CharField(max_length=100)                            # Required Field  
    end_date      = models.CharField(max_length=100)                          # Required Field
    # number_of_question
    # algorithm_id
    def __str__(self) -> str:
        return self
    

class Term(models.Model):
    year_id        = models.ForeignKey(Year, on_delete=models.CASCADE)         # Required Field
    name           = models.CharField(max_length=100)                          # Required Fielded 
    term_number    = models.CharField(max_length=100)                          # Required Field
    # number_of_question
    # algorithm_id
    def __str__(self) -> str:
        return self
    


class Class(models.Model):    
    teacher_id           = models.ForeignKey(User, on_delete=models.CASCADE, default="1") 
    language_id          = models.ForeignKey(Language, on_delete=models.CASCADE, default="1") 
    module_id            = models.ForeignKey(Module, on_delete=models.CASCADE, default="1")  
    term_id              = models.ForeignKey(Term, on_delete=models.CASCADE, default="1")  
    class_code           = models.CharField(max_length=100, null=True)                        # Required Field
    term                 = models.CharField(max_length=100, null=True)                              # Optional Field

    def __str__(self) -> str:
        return self




'''
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
'''
