from typing import Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from applications.main.apps import handle_uploaded_file
from applications.main.forms import AddBuildingObjectForm, AddMaterialsForm
from applications.main.models import BuildingObject, ConstructionMaterial
from framework.custom_logging import logger
from framework.mixins import ExtendedDataContextMixin

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


class MainHome(ExtendedDataContextMixin, ListView):
    model = BuildingObject
    template_name = 'main/index.html'

    def get_queryset(self):
        return BuildingObject.objects.annotate(num_material=Count('constructionmaterial')).order_by('-time_create')

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Список объектов:',
            'mainmenu_selected': 'Главная',
        }
        return context


class ShowBuildingObject(LoginRequiredMixin, ExtendedDataContextMixin, ListView):  # ??????????? detail_view
    model = ConstructionMaterial
    login_url = reverse_lazy('login')
    # redirect_field_name = reverse_lazy('main') ????????????
    success_url = reverse_lazy('main')   # ????????????
    template_name = 'main/object.html'

    def get_queryset(self):
        queryset = ConstructionMaterial.objects.filter(building_object__id=self.kwargs['object_id'])
        logger.debug(queryset)
        return queryset

    def get_extended_context(self) -> Dict:
        context = {
            'title': f"Список материалов по объекту: '{self.b_object_name()}'",
        }
        return context

    def b_object_name(self):
        return BuildingObject.objects.filter(id=self.kwargs['object_id'])[0].name


class AddBuildingObject(LoginRequiredMixin, ExtendedDataContextMixin, CreateView):
    form_class = AddBuildingObjectForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('main')
    template_name = 'main/add_object.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Добавление объекта:',
            'leftmenu_selected': 'Добавить объект',
        }
        return context


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
                    'leftmenu_selected': 'Добавить материалы в объект',
                    'form': form, }
                return render(request, 'main/upload.html', context=context)

            if file.size > 2621440:
                form.add_error('data', 'Файл слишком велик.')
                context = {
                    'mainmenu': menu_v,
                    'leftmenu': menu_h,
                    'title': 'Добавление материалов в объект:',
                    'leftmenu_selected': 'Добавить материалы в объект',
                    'form': form, }
                return render(request, 'main/upload.html', context=context)

            object_id = request.POST['b_object']
            try:
                handle_uploaded_file(file, object_id)
            except IndexError:
                form.add_error('data', 'Структура файла не соответствует шаблону. Смотрите справку.')
                context = {
                    'mainmenu': menu_v,
                    'leftmenu': menu_h,
                    'title': 'Добавление материалов в объект:',
                    'leftmenu_selected': 'Добавить материалы в объект',
                    'form': form, }
                return render(request, 'main/upload.html', context=context)
            else:
                return redirect('object', object_id=object_id)  # redirect in object
    else:
        form = AddMaterialsForm()

    context = {
        'mainmenu': menu_v,
        'leftmenu': menu_h,
        'title': 'Добавление материалов в объект:',
        'leftmenu_selected': 'Добавить материалы в объект',
        'form': form,
    }

    return render(request, 'main/upload.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
