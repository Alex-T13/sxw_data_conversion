from django.urls import path

from applications.auth_reg import views
from applications.main.views import pageNotFound

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
]

handler404 = pageNotFound
