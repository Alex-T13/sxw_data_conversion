from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.main.urls')),
    path('auth/', include('applications.auth_reg.urls')),
]
