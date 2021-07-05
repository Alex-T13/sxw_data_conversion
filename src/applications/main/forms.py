from django import forms
# from django.contrib.auth.models import User

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


class AddMaterialsForm(forms.Form):
    data = forms.FileField(max_length=55, label='Файл для загрузки (*.xlsx)',
                           widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFile'}))
    b_object = forms.ModelChoiceField(queryset=BuildingObject.objects.all(), label='Объект',
                                      widget=forms.Select(attrs={'class': 'form-select', 'type': ''}))

    # def clean_data(self):
    #     data = self.cleaned_data
