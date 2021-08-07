from django import forms

from applications.main.apps import UploadedFileObject
from applications.main.models import BuildingObject
from framework.custom_logging import logger


class AddBuildObjectForm(forms.ModelForm):
    base = forms.CharField(
        max_length=100, required=False, label='База расценок', widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'placeholder': '2017г.', 'disabled': ''}
        )
    )

    class Meta:
        model = BuildingObject
        fields = ['name', 'base']
        widgets = {
            'name': forms.TextInput(attrs={"class": 'form-control', 'type': 'text', 'placeholder': "Название объекта"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddBuildObjectForm, self).__init__(*args, **kwargs)
        self.instance.user = self.request.user
        logger.debug(f"self.instance.user: {self.instance.user}")

    def clean(self):
        super(AddBuildObjectForm, self).clean()
        count_obj = BuildingObject.objects.filter(user__id=self.request.user.id).count()
        if count_obj >= 5:
            raise forms.ValidationError("Вы больше не можете создавать объекты. Вы достигли максимального количества.",
                                        code='overflow')


class AddMaterialsForm(forms.Form):
    data = forms.FileField(
        max_length=100, label="Файл для загрузки (*.xlsx)", widget=forms.FileInput(
            attrs={'class': 'form-control', 'type': 'file', 'id': 'formFile'}
        )
    )
    b_object = forms.ModelChoiceField(
        queryset=BuildingObject.objects.all(), label='Объект', widget=forms.Select(
            attrs={'class': 'form-select', 'type': ''}
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddMaterialsForm, self).__init__(*args, **kwargs)
        self.fields['b_object'].queryset = BuildingObject.objects.filter(user__id=self.request.user.id)

    def clean_data(self):
        data = self.cleaned_data['data']
        logger.debug(f"Content_type: {data.content_type}")
        if data.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise forms.ValidationError("Не верный формат файла, должен быть *.xlsx", code='invalid_content_type')
        if data.size > 2621440:
            raise forms.ValidationError("Файл слишком велик.", code='big_size')
        return data

    def clean(self):
        super(AddMaterialsForm, self).clean()
        try:
            data = self.cleaned_data['data']
        except KeyError:
            raise forms.ValidationError("""Файл не загружается. С ним что-то не так. Обратитесь к разделу 'Помощь'
                                        или оставьте сообщение в разделе 'Отзывы и предложения'""", code='key_error')

        object_id = self.cleaned_data['b_object'].id
        file = UploadedFileObject(data, object_id)

        if not file.check_row_0():
            raise forms.ValidationError("Структура файла не соответствует шаблону. Смотрите справку.", code='index')
        if not file.create_obj_list():
            raise forms.ValidationError("""Данные в файле заполнены не верно. Возможно есть пропущенные пустые ячейки.
                                        Обратитесь к разделу 'Помощь'. (Попробуйте удалить несколько пустых строк в 
                                        конце файла или создать новый файл и скопировать данные в него.)""",
                                        code='type_error')
        if not file.save_in_db():
            raise forms.ValidationError("""При сохранении данных что-то пошло не так. Возможно проблема
                                        кроется в структуре данных Вашего исходного файла. Вы можете оставить сообщение 
                                        в разделе 'Отзывы и предложения'""", code='dbase_error')


class SelectBuildObjectForm(forms.Form):
    b_object = forms.ModelChoiceField(
        queryset=BuildingObject.objects.all(), label='Объект', widget=forms.Select(
            attrs={'class': 'form-select', 'type': ''}
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SelectBuildObjectForm, self).__init__(*args, **kwargs)
        self.fields['b_object'].queryset = BuildingObject.objects.filter(user__id=self.request.user.id)


# ------------------- validators ---------------------

# def validate_comment_word_count(value):
#     count = len(value.split())
#     if count < 30:
#         raise forms.ValidationError(('Please provide at '), params={'count': count},)
