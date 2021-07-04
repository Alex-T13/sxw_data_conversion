from django.urls import path

from applications.upload import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
]
