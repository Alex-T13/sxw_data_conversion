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

    def get_extended_context(self) -> Dict:
        context = {
            'title': 'Детализация сообщения',
        }
        return context


class AllPostView(ExtendedDataContextMixin, ListView):
    model = Post
    template_name = "reviews/all_post.html"

    def get_extended_context(self) -> Dict:
        context = {
            'mainmenu_selected': "Отзывы и предложения",
            'title': "Оставить отзыв",
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


class UpdatePostView(LoginRequiredMixin, ExtendedDataContextMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Post
    form_class = PostForm
    template_name = "reviews/update_post.html"
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        self.object.edited = True
        return super().form_valid(form)

    def get_extended_context(self) -> Dict:
        context = {
            'title': "Редактирование сообщения",
        }
        return context
