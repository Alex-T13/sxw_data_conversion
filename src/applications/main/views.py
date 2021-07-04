from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from applications.main.forms import AddBuildingObjectForm
from applications.main.models import BuildingObject

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


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
