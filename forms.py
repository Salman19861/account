from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createForm(UserCreationForm):
    password2=forms.CharField(widget=forms.PasswordInput(),label='Password (again)')
    class Meta:
        model=User
        fields=['username','email']
        labels={'email':'Email'}