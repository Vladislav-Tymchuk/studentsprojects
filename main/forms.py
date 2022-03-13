from django import forms
from django.forms import ModelForm
from .models import Achievement

class AchievementForm(ModelForm):

    class Meta:
        model = Achievement
        fields = ['achievement', 'name']