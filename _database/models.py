from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.

class Role(models.Model):
    role = models.CharField(max_length=100, null=True)

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
    account_id = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    #def __str__(self) -> str:
        #return self.first_name + " " + self.last_name


class Language(models.Model):
    name = models.CharField(max_length=100, null=True)                          # Required Field

    def __str__(self) -> str:
        return self.name 

class Term(models.Model):
    name           = models.CharField(max_length=100, null=True)                          # Required Fielded 

    def __str__(self) -> str:
        return self.name

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

class Algorithm(models.Model):
    name      = models.CharField(max_length=100, null=True)                          # Required Field
    module = models.ForeignKey(Module, null=True, on_delete=models.SET_NULL)  # The module this algorithm  belongs to
    """
    
    codes = models.ArrayField(
        models.CharField(max_length=100), 
        blank=True,
        null=True
    )
    answers = models.ArrayField(
        models.CharField(max_length=100), 
        blank=True,
        null=True
    )
    hints = models.ArrayField(
        models.CharField(max_length=100), 
        blank=True,
        null=True
    )
    """
    
    def __str__(self) -> str:
        return self.name


class Line(models.Model):
    code      = models.CharField(max_length=100, null=True)                          # Required Field
    answer    = models.CharField(max_length=100, null=True)                          # Required Field
    hint      = models.CharField(max_length=100, null=True, blank=True)                          # Required Field
    algorithm = models.ForeignKey(Algorithm, null=True, on_delete=models.SET_NULL)  # The algorithm this Line  belongs to
    # number_of_question
    # algorithm_id

    def __str__(self) -> str:
        return self.algorithm.name +"-"+ str(self.id)
