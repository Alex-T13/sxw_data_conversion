from django import forms
from django.db import IntegrityError

from applications.main.apps import handle_uploaded_file
from applications.main.models import BuildingObject
from framework.custom_logging import logger


class AddBuildObjectForm(forms.ModelForm):
    class Meta:
        model = BuildingObject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Название объекта'}),
        }


class AddMaterialsForm(forms.Form):
    data = forms.FileField(max_length=100, label='Файл для загрузки (*.xlsx)',
                           widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFile'})
                           )
    b_object = forms.ModelChoiceField(queryset=BuildingObject.objects.all(), label='Объект',
                                      widget=forms.Select(attrs={'class': 'form-select', 'type': ''})
                                      )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddMaterialsForm, self).__init__(*args, **kwargs)

        self.fields['b_object'].queryset = BuildingObject.objects.filter(user__id=self.request.user.id)
        logger.debug(f"request.user.id: {self.request.user.id}")
        logger.debug(f"self.fields['b_object'].queryset_modified: {self.fields['b_object'].queryset}")

    def clean_data(self):
        data = self.cleaned_data['data']
        logger.debug(f"Content_type: {data.content_type}")
        if data.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            raise forms.ValidationError('Не верный формат файла, должен быть *.xlsx', code='invalid content type')
        if data.size > 2621440:
            raise forms.ValidationError('Файл слишком велик.', code='large')
        return data

    def clean(self):
        super(AddMaterialsForm, self).clean()
        logger.debug(f"self.cleaned_data: {self.cleaned_data}")
        try:
            data = self.cleaned_data['data']
        except KeyError:
            raise forms.ValidationError('Файл не загружается. С ним что-то не так. Смотрите справку.', code='key_error')
        object_id = self.cleaned_data['b_object'].id
        logger.debug(f"object_id: {object_id}")

        try:
            handle_uploaded_file(data, object_id)
        except IndexError:
            raise forms.ValidationError('Структура файла не соответствует шаблону. Смотрите справку.', code='index')
        except TypeError:
            raise forms.ValidationError('Данные в файле заполнены не верно. Возможно есть пропущенные пустые ячейки. '
                                        'Смотрите справку. (Попробуйте удалить несколько пустых строк в конце файла '
                                        'или создать новый файл и скопировать данные в него.)', code='type_error')
        except IntegrityError:
            raise forms.ValidationError('При сохранении данных что-то пошло не так. Возможно проблема '
                                        'кроется в структуре данных Вашего исходного файла.', code='dbase_error')


class SelectBuildObjectForm(forms.Form):
    b_object = forms.ModelChoiceField(queryset=BuildingObject.objects.all(), label='Объект',
                                      widget=forms.Select(attrs={'class': 'form-select', 'type': ''})
                                      )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SelectBuildObjectForm, self).__init__(*args, **kwargs)

        self.fields['b_object'].queryset = BuildingObject.objects.filter(user__id=self.request.user.id)
        logger.debug(f"request.user.id: {self.request.user.id}")
        logger.debug(f"self.fields['b_object'].queryset_modified: {self.fields['b_object'].queryset}")


# ------------------- validators ---------------------

# def validate_comment_word_count(value):
#     count = len(value.split())
#     if count < 30:
#         raise forms.ValidationError(('Please provide at '), params={'count': count},)
