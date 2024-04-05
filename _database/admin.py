from django.contrib import admin

# Register your models here.

from .models import *


class ClassAdmin(admin.ModelAdmin):
    filter_horizontal = ('students',)  # This will display the students as a multiple select widget

admin.site.register(Role)
admin.site.register(Account)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Language)
admin.site.register(Term)
admin.site.register(Class, ClassAdmin)
admin.site.register(Module)
admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(Page)
admin.site.register(Algorithm)
admin.site.register(Line)
