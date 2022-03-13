from django.contrib import admin
from .models import Achievement, Teacher, Group, Student

admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Achievement)