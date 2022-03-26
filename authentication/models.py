from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse

class CustomUser(AbstractUser):
    avatar = models.FileField(upload_to='avatars', null=True, blank=True)
    username = models.TextField(max_length = 17, unique=True)
    first_name = models.TextField(max_length = 50)
    last_name = models.TextField(max_length = 50)
    email = models.EmailField(unique=True, blank=True, null=True)
    isTeacher = models.BooleanField(default=False)


    def fullName(self):

        return self.first_name + ' ' + self.last_name