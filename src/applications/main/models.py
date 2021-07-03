from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True, verbose_name='Город')
    birth_date = models.DateField(blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return User.username


class BuildingObject(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название объекта')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('building_object', kwargs={'building_object_id': self.pk})

    class Meta:
        verbose_name = 'Строительный объект'
        verbose_name_plural = 'Строительные объекты'
        ordering = ['-time_create']


class ConstructionMaterial(models.Model):
    title = models.CharField(max_length=31, db_index=True, verbose_name='Обоснование')
    name = models.CharField(max_length=255, db_index=True, verbose_name='Наименование')
    unit = models.CharField(max_length=10, null=True, verbose_name='Ед. измерения')
    quantity = models.DecimalField(max_digits=12, decimal_places=5, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    building_object = models.ForeignKey(BuildingObject, on_delete=models.CASCADE, verbose_name='Строительный объект')
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('construction_material', kwargs={'construction_material_id': self.pk})

    class Meta:
        verbose_name = 'Строительный материал'
        verbose_name_plural = 'Строительные материалы'
        ordering = ['name', 'title']
