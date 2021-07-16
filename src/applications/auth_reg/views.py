from typing import Dict

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.auth_reg.forms import RegisterUserForm
from framework.custom_logging import logger
from framework.mixins import ExtendedDataContextMixin


class RegisterUser(ExtendedDataContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'auth_reg/register.html'
    success_url = reverse_lazy('login')

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Регистрация пользователя:',
            'mainmenu_selected': 'Регистрация/Войти',
        }
        return context


def login(request):
    return HttpResponse("login")


def logout(request):
    return HttpResponse("logout")

