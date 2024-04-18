from django.urls import path
from . import views

#app_name = "versum"

urlpatterns = [
    path('distrib_tech/', views.distrib_tech.as_view(), name='distrib_tech'),
    path('change_rentability/<str:obj_pack>-<str:obj_model>/', views.change_rentability_tech,
    name='change_rentability_tech'),
    path('change_auto_tech/<str:obj_pack>-<str:obj_model>/', views.change_auto_tech,
    name='change_auto_tech'),
    path('change_few_things/<str:obj_pack>-<str:obj_model>/',
    views.change_few_things_obj_tech,
    name='change_few_things_obj_tech'),
    #path('api/media/upload/', views.MediaUploadView.as_view(), name='media-upload'),
]
