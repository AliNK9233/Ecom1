from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms


class registerForm(UserCreationForm):
      class Meta: 
          model = User
          fields = ['username', 'email', 'password1', 'password2']




