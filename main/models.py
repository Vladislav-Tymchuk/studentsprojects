from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models
from django.urls import reverse

from authentication.models import CustomUser


class Teacher(models.Model):
    mainProfile = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    teacherPatronymic = models.TextField(max_length=50)
    teacherSubjects = models.TextField(max_length=127)

    def __str__(self):
        return self.mainProfile.last_name + " " + self.mainProfile.first_name + " " + self.teacherPatronymic
    

    def fullName(self):
        return self.mainProfile.last_name + " " + self.mainProfile.first_name[0] + ". " + self.teacherPatronymic[0] + "."


    def getGroup(self):
        group = Group.objects.get(groupTeacher = self)
        return group

class Group(models.Model):
    groupName = models.TextField(max_length=15, unique=True)
    groupTeacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groupYearAdmission = models.DateField()

    def __str__(self):

        return self.groupName

    def get_url(self):
        
        return reverse('group-info', kwargs={'groupName': self.groupName})

    def get_teacher(self):
        
        return reverse('teacher-info', kwargs={'username': self.groupTeacher.mainProfile.username})


class Student(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.last_name + " " + self.student.first_name + ", группа: " + self.group.groupName

    
    def shortName(self):
        return self.student.last_name + " " + self.student.first_name[0] + "."


class Achievement(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    achievement = models.FileField(upload_to='diplomas')
    name = models.TextField(max_length=127, default='')

    def __str__(self):
        return self.person.last_name + " " + self.person.first_name + " - " + self.name
