# Generated by Django 3.2.6 on 2021-08-20 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_instance', models.IntegerField(default=0)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название объекта')),
                ('base', models.CharField(default='2017г.', max_length=10, verbose_name='База расценок')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Строительный объект',
                'verbose_name_plural': 'Строительные объекты',
                'ordering': ['-time_create'],
            },
        ),
        migrations.CreateModel(
            name='ConstructionMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_instance', models.IntegerField(default=0)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Наименование')),
                ('unit', models.CharField(default='ШТ', max_length=10, verbose_name='Ед. измерения')),
                ('quantity', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=5, max_digits=13, null=True, verbose_name='Цена')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('building_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.buildingobject', verbose_name='Строительный объект')),
            ],
            options={
                'verbose_name': 'Строительный материал',
                'verbose_name_plural': 'Строительные материалы',
                'ordering': ['id_instance', 'name'],
            },
        ),
    ]
