from django.db import models

# Create your models here.

class Student(models.Model):
    firstname    = models.CharField(max_length=100, null=True)
    lastname     = models.CharField(max_length=100, null=True)
    email        = models.EmailField(max_length=100, null=True)
    password     = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    

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


    
