from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy


User = get_user_model()


class Post(models.Model):

    content = models.TextField(max_length=700, verbose_name='Сообщение')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    edited = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    objects = models.Manager()

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse_lazy('object', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-create']
