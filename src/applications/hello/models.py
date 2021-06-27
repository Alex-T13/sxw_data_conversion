from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True, verbose_name='Город')
    birth_date = models.DateField(blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return User.username


class ConstructionMaterial(models.Model):
    title = models.CharField(max_length=31, db_index=True, verbose_name='Обоснование')
    name = models.CharField(max_length=255, db_index=True, verbose_name='Наименование')
    quantity = models.DecimalField(max_digits=12, decimal_places=5, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    material_base = models.ForeignKey('MaterialBase', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MaterialBase(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('BuildingObject', on_delete=models.CASCADE)
    # materials = models
    # file = models.FileField(upload_to='excel_files/', storage='')
    # user_id = models.ForeignKey(on_delete=True)

    def __str__(self):
        return self.title


class BuildingObject(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
