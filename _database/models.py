from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid
from django_ckeditor_5.fields import CKEditor5Field

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

    def __str__(self) -> str:
        return self.account_id.display_name


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
    students = models.ManyToManyField(Account, related_name="student_class", blank=True)

    def __str__(self) -> str:
        return self.class_name
    
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

class Module(models.Model):
    name      = models.CharField(max_length=100, null=True)                          # Required Field
    parent_class = models.ForeignKey(Class, null=True, on_delete=models.SET_NULL)  # The class this module belongs to
    order = models.IntegerField(blank=False, default=100_000)                       # for ordering
    # number_of_question
    # algorithm_id

    def __str__(self) -> str:
        return self.name

class ItemType(models.Model):
    type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'ItemType'
        verbose_name_plural = 'ItemTypes'

class Item(models.Model):
    type = models.ForeignKey(ItemType, null=True, on_delete=models.SET_NULL)
    module = models.ForeignKey(Module, null=True, on_delete=models.SET_NULL)
    order = models.IntegerField(blank=False, default=100_000)                       # for ordering

    def __str__(self) -> str:
        child_item_type = None
        child_item_name = None

        # Check if the child item is a Page
        page = self.page_set.first()
        if page:
            child_item_type = 'Page'
            child_item_name = page.name
            child_item_id = page.id

        # If the child item is not a Page, check if it's an Algorithm
        if not child_item_name:
            algorithm = self.algorithm_set.first()
            if algorithm:
                child_item_type = 'Algorithm'
                child_item_name = algorithm.name
                child_item_id = algorithm.id
        
        #return f"{self.module.name}: {self.type}->{child_item_name}"
        return f"{self.type}->{child_item_name}"
        #return f"[{self.module.id}]: {self.module.name} [{self.id}]: {self.type}  [{child_item_id}]: {child_item_name}"

class Page(models.Model):
    name = models.CharField(max_length=100, null=True) # Required Field
    # content = models.TextField(max_length=2000, null=True) # Required Field 
    content = CKEditor5Field(blank=True, null=True, config_name='extends')
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE) # The module this algorithm

    def __str__(self) -> str:
        return self.name

class Algorithm(models.Model):
    name = models.CharField(max_length=100, null=True) # Required Field
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE) # The module this algorithm  belongs to
    lines = models.TextField(max_length=2000, null=True)
    answers = models.TextField(max_length=2000, null=True)
    hints = models.TextField(max_length=2000, null=True)
    
    def __str__(self) -> str:
        return self.name

class StudentAlgorithm(models.Model):
    student = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    algorithm = models.ForeignKey(Algorithm, null=True, on_delete=models.SET_NULL)
    answers = models.TextField(max_length=2000, null=True)
    score = models.CharField(max_length=20, null=True)
    percentage = models.CharField(max_length=20, null=True)

