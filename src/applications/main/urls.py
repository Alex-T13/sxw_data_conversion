from django.urls import path

from applications.main import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('list_objects/', views.ListObjectsView.as_view(), name='list_objects'),
    path('object/<int:object_id>', views.ShowBuildObjectView.as_view(), name='object'),
    path('add_object/', views.AddBuildObjectView.as_view(), name='add_object'),
    path('clear_object/', views.CleanBuildObjectView.as_view(), name='clear_object'),
    path('del_object/', views.DelBuildObjectView.as_view(), name='del_object'),
    path('upload/', views.UploadFormView.as_view(), name='upload'),
    path('select_dl_obj/', views.SelectDLObjectView.as_view(), name='select_dl_obj'),
    path('download/', views.download_xml, name='download'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('help/', views.HelpView.as_view(), name='help'),
]
