from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from applications.upload.forms import AddMaterialsForm
from applications.upload.apps import handle_uploaded_file
from framework.cutom_logging import logger


menu_v = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Помощь', 'url_name': 'main'},
    {'title': 'Отзывы и предложения', 'url_name': 'main'},
    {'title': 'Регистрация/Войти', 'url_name': 'main'},
]

menu_h = [
    {'title': 'Добавить объект', 'url_name': 'add_object'},
    {'title': 'Добавить материалы в объект', 'url_name': 'upload'},
    {'title': 'Очистить объект', 'url_name': 'add_object'},
    {'title': 'Удалить объект', 'url_name': 'add_object'},
    {'title': 'Скачать данные объекта (xml)', 'url_name': 'add_object'},
]


def upload_file(request):
    if request.method == 'POST':
        form = AddMaterialsForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES.get('data')
            logger.debug(f"Type: {type(request.FILES.get('data'))}")
            logger.debug(f"Type: {request.FILES.get('data').content_type}")
            if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                form.add_error('data', 'Не верный формат файла (*.xlsx)')
                context = {
                    'mainmenu': menu_v,
                    'leftmenu': menu_h,
                    'title': 'Добавление материалов в объект:',
                    'cat_selected': 0,
                    'form': form,}
                return render(request, 'upload/upload.html', context=context)

            if file.size > 2621440:
                form.add_error('data', 'Файл слишком велик.')
                context = {
                    'mainmenu': menu_v,
                    'leftmenu': menu_h,
                    'title': 'Добавление материалов в объект:',
                    'cat_selected': 0,
                    'form': form, }
                return render(request, 'upload/upload.html', context=context)

            handle_uploaded_file(file)

            return redirect('main')  # redirect object
    else:
        form = AddMaterialsForm()

    context = {
        'mainmenu': menu_v,
        'leftmenu': menu_h,
        'title': 'Добавление материалов в объект:',
        'cat_selected': 0,
        'form': form,
    }

    return render(request, 'upload/upload.html', context=context)
