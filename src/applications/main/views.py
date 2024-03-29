import os
from typing import Dict

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, TemplateView, RedirectView

from applications.main.apps import FileXML
from applications.main.forms import AddBuildObjectForm, AddMaterialsForm, SelectBuildObjectForm
from applications.main.models import BuildingObject, ConstructionMaterial
from framework.custom_logging import logger
from framework.mixins import ExtendedDataContextMixin


class MainView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.url = 'list_objects'
        else:
            self.url = 'about'
        url = super(MainView, self).get_redirect_url()
        return url


class ListObjectsView(ExtendedDataContextMixin, ListView):
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


class ShowBuildObjectView(LoginRequiredMixin, ExtendedDataContextMixin, ListView):
    model = ConstructionMaterial
    login_url = reverse_lazy('login')
    template_name = 'main/object.html'

    def get_queryset(self):
        if not BuildingObject.objects.filter(id=self.kwargs['object_id']):
            raise Http404("Страница не найдена")  # HttpResponseNotFound
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


class CleanBuildObjectView(LoginRequiredMixin, ExtendedDataContextMixin, FormView):
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


class DelBuildObjectView(LoginRequiredMixin, ExtendedDataContextMixin, FormView):
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


class SelectDLObjectView(LoginRequiredMixin, ExtendedDataContextMixin, FormView):
    login_url = reverse_lazy('login')

    form_class = SelectBuildObjectForm
    template_name = 'main/select_dl_obj.html'
    success_url = reverse_lazy('download')

    def get_form_kwargs(self):
        kwargs = super(SelectDLObjectView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            object_id = self.request.POST['b_object']
            object_name = str(form.cleaned_data['b_object'])
            user_id = self.request.user.id
            create_xml = FileXML(object_id=object_id, object_name=object_name, user_id=user_id)

            if not create_xml.save_xml_file():
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Скачать данные объекта (xml):',
            'leftmenu_selected': 'Скачать данные объекта (xml)',
        }
        return context


def download_xml(request):
    user_id = request.user.id
    file_name = "Materials.xml"
    file_path = f"{settings.MEDIA_ROOT}/{user_id}/xml/{file_name}"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/xml')
            response['Content-Disposition'] = f"attachment; filename= {os.path.basename(file_path)}"
            return response
    logger.debug("Directory or file does not exist")
    return Http404("Страница не найдена")  # HttpResponseNotFound


class AboutView(ExtendedDataContextMixin, TemplateView):
    template_name = 'main/about.html'

    def get_extended_context(self) -> Dict:
        context = {
            'mainmenu_selected': "О сайте",
            'title': "О сайте"
        }
        return context


class HelpView(ExtendedDataContextMixin, TemplateView):
    template_name = 'main/help.html'

    def get_extended_context(self) -> Dict:
        context = {
            'mainmenu_selected': "Помощь",
            'title': "Справочная информация.",
        }
        return context
