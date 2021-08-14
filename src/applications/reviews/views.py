from typing import Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from applications.reviews.forms import PostForm
from applications.reviews.models import Post
from framework.custom_logging import logger
from framework.mixins import ExtendedDataContextMixin


class ShowPostView(LoginRequiredMixin, ExtendedDataContextMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Post
    template_name = "reviews/post.html"
    # pk_url_kwarg = 'post_id'

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Скачать данные объекта (xml):',
            'mainmenu_selected': 'Объекты',
            'leftmenu_selected': 'Скачать данные объекта (xml)',
        }
        return context


class AllPostView(ExtendedDataContextMixin, ListView):
    model = Post
    template_name = "reviews/all_post.html"

    def get_extended_context(self) -> Dict:
        context = {
            'mainmenu_selected': "Отзывы и предложения",
            'title': "Напишите свой отзыв:",
            'form': PostForm()
        }
        return context


class AddPostView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.author = self.request.user
        logger.debug(f"form.instance.author: {form.instance.author}")
        return super().form_valid(form)


class UpdatePostView(ExtendedDataContextMixin, UpdateView):
    pass

    def get_extended_context(self) -> Dict:
        context = {
            'title': "?????????????",
        }
        return context
