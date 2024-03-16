from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Language)
admin.site.register(Module)
admin.site.register(Term)
admin.site.register(Year)