from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms



class SignupForm(UserCreationForm):
    phone = forms.CharField(max_length=20)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'age')




