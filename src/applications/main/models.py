from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class BuildingObject(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название объекта')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('object', kwargs={'object_id': self.pk})

    class Meta:
        verbose_name = 'Строительный объект'
        verbose_name_plural = 'Строительные объекты'
        ordering = ['-time_create']


class ConstructionMaterial(models.Model):

    id_instance = models.IntegerField(default=0,)
    name = models.CharField(max_length=255, db_index=True, verbose_name='Наименование')
    unit = models.CharField(max_length=10, null=True, verbose_name='Ед. измерения')
    quantity = models.DecimalField(max_digits=12, decimal_places=5, verbose_name='Количество')
    price = models.DecimalField(max_digits=13, decimal_places=5, null=True, verbose_name='Цена')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    building_object = models.ForeignKey(BuildingObject, on_delete=models.CASCADE, verbose_name='Строительный объект')
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('material', kwargs={'material_id': self.pk})

    class Meta:
        verbose_name = 'Строительный материал'
        verbose_name_plural = 'Строительные материалы'
        ordering = ['id_instance', 'name']
