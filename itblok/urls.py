from django.urls import path
from . import views
#from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

#app_name = "itblok"

urlpatterns = [
path('distrib_itblok_comps/', views.ItComps.as_view(), name='itblok_comps'),
path('it_margin_exch/<str:it_pk>/', views.it_margin_exch,
name='it_margin_exch'),
path('edit_it_num_fan/<str:comp_pack>/', views.edit_it_num_fan,
name='edit_it_num_fan'),
path('change_label/<str:obj_pack>/', views.change_label,
name='change_label'),
path('itblok_edit_parts_pack/<str:comp_pack>/', views.edit_parts_pack,
name='itblok_edit_parts_pack'),
]
