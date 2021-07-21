from typing import Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView

from applications.main.forms import AddBuildingObjectForm, AddMaterialsForm
from applications.main.models import BuildingObject, ConstructionMaterial
from framework.mixins import ExtendedDataContextMixin


class MainHome(ExtendedDataContextMixin, ListView):
    model = BuildingObject
    template_name = 'main/index.html'

    def get_queryset(self):
        return BuildingObject.objects.annotate(num_material=Count('constructionmaterial')).order_by('-time_create')

    def get_extended_context(self) -> Dict:
        context = {
            'mainmenu_selected': 'Главная',
        }
        if self.request.user.is_authenticated:
            context['title'] = 'Список объектов:'
        return context


class ShowBuildingObject(LoginRequiredMixin, ExtendedDataContextMixin, ListView):  # ??????????? detail_view
    model = ConstructionMaterial
    login_url = reverse_lazy('login')
    # redirect_field_name = reverse_lazy('main') ????????????
    success_url = reverse_lazy('main')   # ????????????
    template_name = 'main/object.html'

    def get_queryset(self):
        queryset = ConstructionMaterial.objects.filter(building_object__id=self.kwargs['object_id'])
        return queryset

    def get_extended_context(self) -> Dict:
        context = {
            'title': f"Список материалов по объекту: '{self.b_object_name()}'",
        }
        return context

    def b_object_name(self):
        return BuildingObject.objects.filter(id=self.kwargs['object_id'])[0].name


class AddBuildingObject(LoginRequiredMixin, ExtendedDataContextMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = AddBuildingObjectForm
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


class UploadFormView(LoginRequiredMixin, ExtendedDataContextMixin, FormView):
    login_url = reverse_lazy('login')
    form_class = AddMaterialsForm
    template_name = 'main/upload.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Добавление материалов в объект:',
            'leftmenu_selected': 'Добавить материалы в объект',
        }
        return context

    def get_success_url(self):
        object_id = self.request.POST['b_object']
        return reverse_lazy('object', kwargs={'object_id': object_id})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
