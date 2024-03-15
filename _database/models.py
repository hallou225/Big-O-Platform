from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.

class TeacherManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class Teacher(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True)            # Required Field
    middle_name = models.CharField(max_length=100, null=True, blank=True)           # Optional Field
    last_name = models.CharField(max_length=100, null=True)             # Required Field
    display_name = models.CharField(max_length=100, null=True, blank=True)          # Optional Field
    username = models.CharField(max_length=100, null=True, unique=True) # Required Identifier
    email = models.EmailField(max_length=250, null=True, unique=True)   # Required Field
    date_created = models.DateTimeField(auto_now_add=True)              # No Specification Required

    last_login = models.DateTimeField(auto_now=True, null=True)
    is_staff = models.BooleanField(default=False)                   # Not staff
    is_active = models.BooleanField(default=True)                   # Account is active initially
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username
    
    objects = TeacherManager()

    def get_by_natural_key(self, username):
        return self.get(username=username)
    
    def save(self, *args, **kwargs):
        if not self.display_name and self.first_name and self.last_name:
            self.display_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

'''
class Teacher(AbstractUser):
    first_name = models.CharField(max_length=100, null=True)        # Required Field
    middle_name = models.CharField(max_length=100, null=True)       # Optional Field
    last_name = models.CharField(max_length=100, null=True)         # Required Field
    display_name = models.CharField(max_length=100, null=True)      # Optional Field
    username = models.CharField(max_length=100, null=True, unique=True)          # Required Field
    password = models.CharField(max_length=100, null=True)          # Required Field
    email = models.EmailField(max_length=250, null=True)             # Required Field
    date_created = models.DateTimeField(auto_now_add=True)          # No Specification Required

    last_login = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.username
'''
    
class Student(models.Model):
    first_name = models.CharField(max_length=100, null=True)         # Required Field
    middle_name = models.CharField(max_length=100, null=True)        # Optional Field
    last_name = models.CharField(max_length=100, null=True)          # Required Field
    username = models.CharField(max_length=100, null=True)           # Required Field
    password = models.CharField(max_length=100, null=True)           # Required Field
    email = models.CharField(max_length=100, null=True)              # Required Field
    date_created = models.DateTimeField(auto_now_add=True)           # No Specification Required

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class Class(models.Model):
    class_name = models.CharField(max_length=100, null=True)                        # Required Field
    class_code = models.CharField(max_length=100, null=True, unique=True)                        # Required Field
    term = models.CharField(max_length=100, null=True)                              # Optional Field
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)      # Points to Teacher Model
        # when a teacher account is deleted, any classes associated with that account 
        # will remain in the database, with a null value for teacher
    #module_id = 

    def __str__(self) -> str:
        return self.class_name
    
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'



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
