from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from applications.main.models import BuildingObject


# class AddBuildingObjectForm(forms.ModelForm):
#     class Meta:
#         model = BuildingObject
#         fields = ['name', 'user']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Название объекта'}),
#             # 'is_hidden'  <input type="hidden" ...>
#             'user': forms.Select(attrs={'class': 'form-select', 'type': ''}),
#         }
#
#
# class AddMaterialsForm(forms.Form):
#     data = forms.FileField(max_length=55, label='Файл для загрузки (*.xlsx)',
#                            widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFile'}))
#     b_object = forms.ModelChoiceField(queryset=BuildingObject.objects.all(), label='Объект',
#                                       widget=forms.Select(attrs={'class': 'form-select', 'type': ''}))
#
#     # def clean_data(self):
#     #     data = self.cleaned_data

class RegisterUserForm(UserCreationForm):
    # username = forms.CharField(label='Логин*', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # email = forms.EmailField(label='Email*', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    # password1 = forms.CharField(label='Пароль*', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # password2 = forms.CharField(label='Повтор пароля*', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Логин*'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Фамилия'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email*'}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Пароль*'}),
            'password2': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Повтор пароля*'}),
        }
