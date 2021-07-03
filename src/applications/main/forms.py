from django import forms
from django.contrib.auth.models import User

from applications.main.models import BuildingObject


class AddBuildingObjectForm(forms.ModelForm):
    class Meta:
        model = BuildingObject
        fields = ['name', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Название объекта'}),
            # 'is_hidden'  <input type="hidden" ...>
            'user': forms.Select(attrs={'class': 'form-select', 'type': ''}),
        }




