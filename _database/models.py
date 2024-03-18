from django.db import models
<<<<<<< HEAD
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
=======
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.

class Role(models.Model):
    role = models.CharField(max_length=100, null=True)
>>>>>>> 1235018a74387affbfdd771b7c77a52f7d83a544

    def __str__(self):
        return self.role

class AccountManager(BaseUserManager):
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

class Account(AbstractBaseUser, PermissionsMixin):
    roleArray = [
        ("student", "student"),
        ("teacher", "teacher")
    ]
    first_name = models.CharField(max_length=100, null=True)            # Required Field
    middle_name = models.CharField(max_length=100, null=True, blank=True)           # Optional Field
    last_name = models.CharField(max_length=100, null=True)             # Required Field
    display_name = models.CharField(max_length=100, null=True, blank=True)          # Optional Field
    username = models.CharField(max_length=100, null=True, unique=True) # Required Identifier
    email = models.EmailField(max_length=250, null=True, unique=True)   # Required Field
    #role = models.CharField(max_length=10, null=True, choices=roleArray)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)              # No Specification Required

    last_login = models.DateTimeField(auto_now=True, null=True)
    is_staff = models.BooleanField(default=False)                   # Not staff
    is_active = models.BooleanField(default=True)                   # Account is active initially
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username
    
    objects = AccountManager()

    def get_by_natural_key(self, username):
        return self.get(username=username)
    
    def save(self, *args, **kwargs):
        if not self.display_name and self.first_name and self.last_name:
            self.display_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

class Teacher(models.Model):
    account_id = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    #def __str__(self) -> str:
        #return self.first_name + " " + self.last_name
    
class Student(models.Model):
<<<<<<< HEAD
    first_name   = models.CharField(max_length=100, null=True)         # Required Field
    middle_name  = models.CharField(max_length=100, null=True)        # Optional Field
    last_name    = models.CharField(max_length=100, null=True)          # Required Field
    username     = models.CharField(max_length=100, null=True)           # Required Field
    password     = models.CharField(max_length=100, null=True)           # Required Field
    email        = models.CharField(max_length=100, null=True)              # Required Field
    date_created = models.DateTimeField(auto_now_add=True)           # No Specification Required
=======
    account_id = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    #def __str__(self) -> str:
        #return self.first_name + " " + self.last_name


class Language(models.Model):
    name = models.CharField(max_length=100, null=True)                          # Required Field
>>>>>>> 1235018a74387affbfdd771b7c77a52f7d83a544

    def __str__(self) -> str:
        return self.name 

class Term(models.Model):
    name           = models.CharField(max_length=100, null=True)                          # Required Fielded 

    def __str__(self) -> str:
        return self.name

<<<<<<< HEAD
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
=======
class Class(models.Model):
    class_name = models.CharField(max_length=100, null=True)                        # Required Field
    class_code = models.CharField(max_length=100, null=True, unique=True)                        # Required Field
    term = models.ForeignKey(Term, null=True, on_delete=models.SET_NULL)                              # Optional Field
    teacher = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)      # Points to Teacher Model
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL, blank=True)
        # when a teacher account is deleted, any classes associated with that account 
        # will remain in the database, with a null value for teacher

    def __str__(self) -> str:
        return self.class_name
>>>>>>> 1235018a74387affbfdd771b7c77a52f7d83a544
    
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

class Module(models.Model):
    name      = models.CharField(max_length=100, null=True)                          # Required Field
    parent_class = models.ForeignKey(Class, null=True, on_delete=models.SET_NULL)  # The class this module belongs to
    # number_of_question
    # algorithm_id

    def __str__(self) -> str:
        return self.name
