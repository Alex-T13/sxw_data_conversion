from django import forms

from applications.main.models import BuildingObject


class AddMaterialsForm(forms.Form):
    data = forms.FileField()
    b_object = forms.ModelChoiceField(queryset=BuildingObject.objects.all())
