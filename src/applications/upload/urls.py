from django.urls import path

from applications.main import views

urlpatterns = [
    path('', views.index, name='upload'),
]
