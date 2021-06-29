from django.urls import path

from applications.hello import views

urlpatterns = [
    path('', views.index, name='upload'),
]
