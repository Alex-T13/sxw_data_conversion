from django.urls import path

from applications.main import views

urlpatterns = [
    path('', views.index, name='main'),
    path('add_object/', views.add_building_object, name='add_object'),
]
