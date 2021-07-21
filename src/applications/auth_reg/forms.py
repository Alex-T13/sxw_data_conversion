from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Логин* ', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.EmailField(max_length=100, required=True, label='Email* ', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'type': 'email'}))
    password1 = forms.CharField(max_length=100, label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    password2 = forms.CharField(max_length=100, label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'id': 'inputUsername'}))
    password = forms.CharField(max_length=100, label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'id': 'inputPassword'}))

