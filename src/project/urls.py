from django.contrib import admin
from django.urls import path, include
# from applications.main.views import pageNotFound


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.main.urls')),
    path('auth/', include('applications.auth_reg.urls')),
    path('reviews/', include('applications.reviews.urls')),
]

# handler404 = pageNotFound
