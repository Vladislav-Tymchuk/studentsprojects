from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.FileField(upload_to='avatars', null=True, blank=True)
    username = models.CharField(max_length = 17, unique=True)
    last_name = models.CharField(max_length = 50)
    first_name = models.CharField(max_length = 50)
    patronymic = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(unique=True, default='')
    isTeacher = models.BooleanField(default=False)
    userGroup = models.ManyToManyField('main.Group', default=None)


    def fullName(self):

        return self.last_name + ' ' + self.first_name


    def fullTeacherName(self):
        return self.last_name + " " + self.first_name[0] + ". " + self.patronymic[0] + "."