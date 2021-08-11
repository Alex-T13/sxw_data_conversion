from django.urls import path

from applications.main import views

urlpatterns = [
    path('', views.MainHomeView.as_view(), name='main'),
    path('object/<int:object_id>', views.ShowBuildingObjectView.as_view(), name='object'),
    path('add_object/', views.AddBuildObjectView.as_view(), name='add_object'),
    path('clear_object/', views.CleanBuildObjectView.as_view(), name='clear_object'),
    path('del_object/', views.DelBuildObjectView.as_view(), name='del_object'),
    path('upload/', views.UploadFormView.as_view(), name='upload'),
    path('select_dl_obj/', views.SelectDLObjectView.as_view(), name='select_dl_obj'),
    path('download/', views.download_xml, name='download'),
    path('help/', views.MainHomeView.as_view(), name='help'),
]
