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

urlpatterns = [
    path('pas/', views.main_password2, name='main_password2'),
    path('', views.main_password, name='main_password'),
    path('main', views.home, name='cat-home'),
    path('price', views.price, name='cat-price'),
    path('price/<str:price_id>/', views.kind_price, name='kind_price'),
    path('assembly_page/<str:page_id>/', views.pc_assembly_page, name='assembly_page'),
    path('assembly/<int:pc_id>/', views.pc_assembly, name='assembly'),
    #path('home/assembly/comp/<int:pc_id>-<str:itm>/', views.test, name='test'),
    path('assembly/comp/<int:pc_id>-<int:itm>/', views.kind_price_item, name='assembly_item'),
    path('assembly/comp_all/<int:pc_id>-<int:itm>/', views.kind_price_item_all, name='assembly_item_all'),
    #path('<str:price_id>/', views.Views_kind_price.as_view(), name='kind_price'),
    path('compnew/<int:pc_ass>', views.computercreate, name='computercreate'),
    path('test_price/<int:d>', views.test_price, name='test_price'),
    path('test_assembly/<int:short_id>-<int:id_>-<int:pc_id>/', views.test_assembly, name='test_assembly'),
    path('forversum/<str:i>-<int:id>', views.forversum, name='forversum'),
    path('advanced_reserve/<int:page_id>-<str:price>-<int:grp>', views.pc_assembly_page_advanced, name='pc_assembly_page_advanced'),
    path('price_itblok/<int:id>', views.for_itblok, name='for_itblok'),
]

