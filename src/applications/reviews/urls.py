from django.urls import path

from applications.reviews import views

urlpatterns = [
    path('', views.AllPostView.as_view(), name='reviews'),
    path('add_post', views.AddPostView.as_view(), name='add_post'),
    path('post/<int:pk>', views.ShowPostView.as_view(), name='post'),
    # path('object/<int:object_id>', views.ShowBuildingObjectView.as_view(), name='object'),
    # path('update_post/<int:pk>', views.PostView.as_view(), name='update_post'),
]
