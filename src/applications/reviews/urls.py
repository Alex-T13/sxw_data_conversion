from django.urls import path

from applications.reviews import views

urlpatterns = [
    path('', views.AllPostView.as_view(), name='reviews'),
    path('add_post', views.AddPostView.as_view(), name='add_post'),
    path('post/<int:pk>', views.ShowPostView.as_view(), name='post'),
    path('update_post/<int:pk>', views.UpdatePostView.as_view(), name='update_post'),
]
