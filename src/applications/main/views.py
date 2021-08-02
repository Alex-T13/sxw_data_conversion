import os
from typing import Dict

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponseNotFound, HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView

from applications.main.apps import create_xml
from applications.main.forms import AddBuildObjectForm, AddMaterialsForm, SelectBuildObjectForm
from applications.main.models import BuildingObject, ConstructionMaterial
from framework.custom_logging import logger
from framework.mixins import ExtendedDataContextMixin


class MainHomeView(ExtendedDataContextMixin, ListView):
    model = BuildingObject
    template_name = 'main/index.html'

    def get_queryset(self):
        return BuildingObject.objects.filter(
            user__id=self.request.user.id).annotate(num_material=Count('constructionmaterial')).order_by('-time_create')

    def get_extended_context(self) -> Dict:
        context = {
            'mainmenu_selected': 'Объекты',
        }
        if self.request.user.is_authenticated:
            context['title'] = 'Список объектов:'

        if not self.object_list:
            context['title'] = 'У Вас пока нет созданных объектов.'
        return context


class ShowBuildingObjectView(LoginRequiredMixin, ExtendedDataContextMixin, ListView):
    model = ConstructionMaterial
    login_url = reverse_lazy('login')
    template_name = 'main/object.html'

    def get_queryset(self):
        if not BuildingObject.objects.filter(id=self.kwargs['object_id']):
            raise Http404("Страница не найдена")
        queryset = ConstructionMaterial.objects.filter(building_object__id=self.kwargs['object_id'])
        return queryset

    def get_extended_context(self) -> Dict:
        context = {
            'title': self.b_object_name(),
            'sum_mat': self.sum_mat(),
        }
        return context

    def b_object_name(self):
        b_object_name = f'Список материалов по объекту: "{self.object_list[0].building_object}"' \
            if self.object_list else f'Нет материалов привязанных к этому объекту.'
        return b_object_name

    def sum_mat(self):
        return self.object_list.aggregate(sum_mat=Sum('total_cost')).get('sum_mat')


class AddBuildObjectView(LoginRequiredMixin, ExtendedDataContextMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = AddBuildObjectForm
    success_url = reverse_lazy('main')
    template_name = 'main/add_object.html'

    def get_form_kwargs(self):
        kwargs = super(AddBuildObjectView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    # def form_valid(self, form):
    #     # logger.debug(f"form.instance: {form.instance}")
    #
    #     form.instance.user = self.request.user
    #     logger.debug(f"form.instance.user: {form.instance.user}")
    #     return super().form_valid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Добавление объекта:',
            'leftmenu_selected': 'Создать объект',
        }
        return context


class UploadFormView(LoginRequiredMixin, ExtendedDataContextMixin, FormView):
    login_url = reverse_lazy('login')

    form_class = AddMaterialsForm
    template_name = 'main/upload.html'

    def get_form_kwargs(self):
        kwargs = super(UploadFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Добавление материалов в объект:',
            'leftmenu_selected': 'Добавить материалы в объект',
        }
        return context

    def get_success_url(self):
        object_id = self.request.POST['b_object']
        return reverse_lazy('object', kwargs={'object_id': object_id})


class CleanBuildObjectView(LoginRequiredMixin, ExtendedDataContextMixin, FormView, ):
    login_url = reverse_lazy('login')

    form_class = SelectBuildObjectForm
    success_url = reverse_lazy('main')
    template_name = 'main/clean_object.html'

    def get_form_kwargs(self):
        kwargs = super(CleanBuildObjectView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            logger.debug(f"self.request.POST['b_object']: {self.request.POST['b_object']}")
            ConstructionMaterial.objects.filter(building_object__id=self.request.POST['b_object']).delete()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Удаление всех материалов объекта:',
            'leftmenu_selected': 'Очистить объект',
        }
        return context


class DelBuildObjectView(LoginRequiredMixin, ExtendedDataContextMixin, FormView,):
    login_url = reverse_lazy('login')

    form_class = SelectBuildObjectForm
    success_url = reverse_lazy('main')
    template_name = 'main/del_object.html'

    def get_form_kwargs(self):
        kwargs = super(DelBuildObjectView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            logger.debug(f"self.request.POST['b_object']: {self.request.POST['b_object']}")
            BuildingObject.objects.filter(pk=self.request.POST['b_object']).delete()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Удаление объекта:',
            'leftmenu_selected': 'Удалить объект',
        }
        return context


class SelectDLObjectView(LoginRequiredMixin, ExtendedDataContextMixin, FormView,):
    login_url = reverse_lazy('login')

    form_class = SelectBuildObjectForm
    template_name = 'main/select_dl_obj.html'

    def get_form_kwargs(self):
        kwargs = super(SelectDLObjectView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            logger.debug(f"self.request.POST['b_object']: {self.request.POST['b_object']}")
            object_id = self.request.POST['b_object']
            logger.debug(f"self.request.user.id: {self.request.user.id}")
            user_id = self.request.user.id

            create_xml(object_id=object_id, user_id=user_id)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Скачать данные объекта (xml):',
            'leftmenu_selected': 'Скачать данные объекта (xml)',
        }
        return context

    def get_success_url(self):
        object_id = self.request.POST['b_object']
        return reverse_lazy('download', kwargs={'object_id': object_id})


def download_xml(request, **kwargs):
    object_id = kwargs['object_id']
    logger.debug(f"kwargs['object_id']: {kwargs['object_id']}")

    user_id = request.user.id
    logger.debug(f"request.user.id: {request.user.id}")

    file_name = f"Materials_obj{object_id}.xml"
    file_path = f"{settings.MEDIA_ROOT}/{user_id}/xml/{file_name}"

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='text/xml')
            response['Content-Disposition'] = f"attachment; filename= {os.path.basename(file_path)}"
            return response


# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1>Страница не найдена</h1>')
