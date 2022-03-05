from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'first_name', 'last_name', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Почта уже существует')
        return email

    def clean_username(self):
        if CustomUser.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('Данный пользователь уже существует')
        return self.cleaned_data['username']

class CustomUserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'first_name', 'last_name']