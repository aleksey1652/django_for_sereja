"""samplesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

#app_name = "versum" 

urlpatterns = [
    path('uploader/<str:w>', views.uploader, name='uploader'),
    path('compare/<str:duo>', views.compare_sites, name='compare_sites'),
    path('parts/<int:p>-<str:w>', views.get_parts_on_site, name='get_parts_on_site'),
    path('parts/hdd/<int:p>', views.get_hdd_on_site, name='get_hdd_on_site'),
    path('parts/price/<int:p0>-<int:p1>', views.get_price_on_site, name='get_price_on_site'),
    path('negativ/', views.get_negative_margin, name='get_negative_margin'),
    path('article/', views.articlecreate, name='articlecreate'),
    path('article_start/<int:p>', views.articlestart, name='articlestart'),
    path('send/<str:p>', views.send_sheet, name='send_sheet'),
    path('sendparts/', views.send_sheet_parts, name='send_sheet_parts'),
    path('positiv/', views.get_positive_margin, name='get_positive_margin'),
    path('distrib/', views.versum_api.as_view(), name='versum'),
    path('distrib2/', views.versum_api_parts.as_view(), name='versum_parts'),
    path('mark_comps_parts/', views.mark_comps_parts.as_view(), name='mark_comps_parts'),
    path('distrib_itblok/', views.itblok_api.as_view(), name='itblok'),
    path('distrib_promotin/', views.versum_api_promotin.as_view(), name='versum_promotin'),
    path('distrib_comps_promotin/', views.versum_api_comps_promotin.as_view(),
    name='comps_promotin'),
    path('distrib_single_parts/', views.versum_single_parts.as_view(), name='single_parts'),
    path('distrib_new/', views.versum_api_new.as_view(), name='versum_api_new'),
    path('distrib_newest/', views.Versum_api_newest.as_view(), name='versum_api_newest'),
    path('desk/<str:series>-<str:lang>', views.get_kind_assembly_desc,
    name='get_kind_assembly_desc'),
    path('example/', views.webhook, name='webhook'),
    path('media/images/', views.MediaUploadView.as_view(), name='media_upload'),
]
