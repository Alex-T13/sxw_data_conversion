from typing import Dict

from django.http import HttpResponse
from django.views.generic import ListView

from applications.reviews.models import Post
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
        }
        return context
