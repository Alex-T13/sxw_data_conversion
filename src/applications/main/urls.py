from django.urls import path

from applications.main import views
from applications.main.views import pageNotFound

urlpatterns = [
    path('', views.MainHome.as_view(), name='main'),
    path('object/<int:object_id>', views.ShowBuildingObject.as_view(), name='object'),
    path('add_object/', views.AddBuildingObject.as_view(), name='add_object'),
    path('upload/', views.upload_file, name='upload'),
]

handler404 = pageNotFound
