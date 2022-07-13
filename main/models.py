from django.db import models
from django.urls import reverse

from authentication.models import CustomUser


class Group(models.Model):
    groupName = models.CharField(max_length=15, unique=True)
    groupTeacher = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    groupYearAdmission = models.DateField()


    def __str__(self):

        return self.groupName

    def get_url(self):
        
        return reverse('group-info', kwargs={'groupName': self.groupName})

    def get_teacher(self):
        
        return reverse('teacher-info', kwargs={'username': self.groupTeacher.username})


class Achievement(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    achievement = models.FileField(upload_to='diplomas')
    name = models.CharField(max_length=127, default='')

    def __str__(self):
        return self.person.fullName() + " - " + self.name
