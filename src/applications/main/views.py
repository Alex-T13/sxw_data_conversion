from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from applications.main.apps import handle_uploaded_file
from applications.main.forms import AddBuildingObjectForm, AddMaterialsForm
from applications.main.models import BuildingObject
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


def index(request):
    b_objects = BuildingObject.objects.all()

    context = {
        'b_objects': b_objects,
        'mainmenu': menu_v,
        'leftmenu': menu_h,
        'title': 'Список объектов:',
        'cat_selected': 0,
    }
    return render(request, 'main/index.html', context=context)


def add_building_object(request):
    if request.method == 'POST':
        form = AddBuildingObjectForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('main')
    else:
        form = AddBuildingObjectForm()

    context = {
        'mainmenu': menu_v,
        'leftmenu': menu_h,
        'title': 'Добавление объекта:',
        'cat_selected': 0,
        'form': form,
    }

    return render(request, 'main/add_object.html', context=context)


def upload_file(request):
    if request.method == 'POST':
        form = AddMaterialsForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES.get('data')
            logger.debug(f"Type: {type(request.FILES.get('data'))}")
            logger.debug(f"Content_ype: {request.FILES.get('data').content_type}")
            if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                form.add_error('data', 'Не верный формат файла (*.xlsx)')
                context = {
                    'mainmenu': menu_v,
                    'leftmenu': menu_h,
                    'title': 'Добавление материалов в объект:',
                    'cat_selected': 0,
                    'form': form, }
                return render(request, 'main/upload.html', context=context)

            if file.size > 2621440:
                form.add_error('data', 'Файл слишком велик.')
                context = {
                    'mainmenu': menu_v,
                    'leftmenu': menu_h,
                    'title': 'Добавление материалов в объект:',
                    'cat_selected': 0,
                    'form': form, }
                return render(request, 'main/upload.html', context=context)

            handle_uploaded_file(file)

            return redirect('main')  # redirect in object
    else:
        form = AddMaterialsForm()

    context = {
        'mainmenu': menu_v,
        'leftmenu': menu_h,
        'title': 'Добавление материалов в объект:',
        'cat_selected': 0,
        'form': form,
    }

    return render(request, 'main/upload.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
