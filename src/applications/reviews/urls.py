from django.urls import path

from applications.reviews import views

urlpatterns = [
    path('', views.AllPostView.as_view(), name='reviews'),

]
