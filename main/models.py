from distutils.command.upload import upload
from django.db import models
from django.urls import reverse

from authentication.models import CustomUser


class Teacher(models.Model):
    teacherPhoto = models.ImageField(upload_to='teachers-photos')
    teacherSurname = models.TextField(max_length=50)
    teacherName = models.TextField(max_length=50)
    teacherPatronymic = models.TextField(max_length=50)
    teacherSubjects = models.TextField(max_length=127)

    def __str__(self):
        return self.teacherSurname + " " + self.teacherName + " " + self.teacherPatronymic
    

    def fullName(self):
        return self.teacherSurname + " " + self.teacherName


class Group(models.Model):
    groupName = models.TextField(max_length=15)
    groupTeacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    groupYearAdmission = models.DateField()

    def __str__(self):

        return self.groupName

    def get_url(self):
        
        return reverse('group-info', kwargs={'groupName': self.groupName})

    def get_teacher(self):
        
        return reverse('teacher-info', kwargs={'pk': self.groupTeacher.id})


class Student(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.last_name + " " + self.student.first_name + ", группа: " + self.group.groupName


class Achievement(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    achievement = models.FileField(upload_to='diplomas')
    name = models.TextField(max_length=127, default='')

    def __str__(self):
        return self.student.last_name + " " + self.student.first_name + " - " + self.name
