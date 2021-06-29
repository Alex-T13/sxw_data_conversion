from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from applications.hello.models import BuildingObject

menu_vert = ["Главная", "Помощь", "Отзывы и предложения", "Регистрация/Войти"]

menu_horiz = ["Добавить объект", "Добавить материалы в объект", "Очистить объект", "Удалить объект",
              "Скачать данные объекта (xml)"]


def index(request):
    user = User.objects.all()
    return render(request, 'hello/_base.html', {'user': user, 'menu': menu_horiz, 'title': 'Главная страница'})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')