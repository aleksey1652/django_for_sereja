from django.urls import path
from . import views

#app_name = "versum"

urlpatterns = [
    path('distrib_single_parts/', views.versum_single_parts.as_view(), name='single_parts'),
    path('change_rentability/<str:obj_pack>-<str:obj_model>/', views.change_rentability_obj,
    name='change_rentability_obj'),
    path('change_auto/<str:obj_pack>-<str:obj_model>/', views.change_auto_obj,
    name='change_auto_obj'),
    path('change_few_things_obj/<str:obj_pack>-<str:obj_model>/', views.change_few_things_obj,
    name='change_few_things_obj'),
    #path('api/media/upload/', views.MediaUploadView.as_view(), name='media-upload'),
]
