from django import forms

from applications.main.models import BuildingObject


class AddBuildingObjectForm(forms.ModelForm):
    class Meta:
        model = BuildingObject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Название объекта'}),
        }


class AddMaterialsForm(forms.Form):
    data = forms.FileField(max_length=55, label='Файл для загрузки (*.xlsx)',
                           widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFile'}))
    b_object = forms.ModelChoiceField(queryset=BuildingObject.objects.all(), label='Объект',
                                      widget=forms.Select(attrs={'class': 'form-select', 'type': ''}))

