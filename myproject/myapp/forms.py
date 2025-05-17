from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'password1', 'password2']
