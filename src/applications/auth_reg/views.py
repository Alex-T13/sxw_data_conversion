from typing import Dict

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.auth_reg.forms import RegisterUserForm, LoginUserForm
from framework.mixins import ExtendedDataContextMixin


class RegisterUser(ExtendedDataContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'auth_reg/register.html'

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Регистрация пользователя:',
            'mainmenu_selected': 'Регистрация',
        }
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(ExtendedDataContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'auth_reg/login.html'
    # success_url = reverse_lazy('main')

    def get_success_url(self):
        return reverse_lazy('main')

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Авторизация:',
            'mainmenu_selected': 'Вход',
        }
        return context


class LogoutUser(LogoutView):
    template_name = 'auth_reg/logout.html'
