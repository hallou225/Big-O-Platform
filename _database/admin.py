from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Role)
admin.site.register(Account)
admin.site.register(Teacher)
admin.site.register(Student)
<<<<<<< HEAD
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Language)
admin.site.register(Module)
admin.site.register(Term)
admin.site.register(Year)
=======
admin.site.register(Language)
admin.site.register(Term)
admin.site.register(Class)
admin.site.register(Module)
>>>>>>> 1235018a74387affbfdd771b7c77a52f7d83a544
