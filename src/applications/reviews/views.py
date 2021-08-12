from typing import Dict

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from applications.reviews.forms import PostForm
from applications.reviews.models import Post
from framework.custom_logging import logger
from framework.mixins import ExtendedDataContextMixin


class AllPostView(ExtendedDataContextMixin, ListView):
    model = Post
    template_name = "reviews/all_post.html"

    # def get_queryset(self):
    #     return Post.objects.all()

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
    # template_name = "reviews/all_post.html"
    form_class = PostForm
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.author = self.request.user
        logger.debug(f"form.instance.user: {form.instance.author}")
        return super().form_valid(form)
