from django.urls import path

from applications.auth_reg import views
from applications.main.views import pageNotFound

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
]

handler404 = pageNotFound
