from django.urls import path
from . import views
#from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

#app_name = "versum" promotions_admin_edit admin_special_price

urlpatterns = [
    #path('admin/', admin.site.urls, name='admin'),
    path('statistics/', views.webhook, name='webhook'),
    path('', views.Family, name='family'),
    path('family/<str:st_pk>/', views.Family, name='family'),
    path('kurier_periods/<str:st_pk>/<int:ss_pk>/', views.kurier_periods,
    name='kurier_periods'),
    path('kurier_del/<str:kb_pk>/', views.kurier_del, name='kurier_del'),
    path('bids/<int:pk>', views.BidsDetailView.as_view(), name='bids-detail'),
    path('admin_test/ya/<str:test_pk>/', views.admin_test, name='admin_test'),
    path('admin_delete_relate/ya/<str:test_pk>/', views.admin_delete_relate,
    name='admin_delete_relate'),
    path('catch_to_admin/<str:what>/<str:short_name>/', views.catch_to_admin_forms,
    name='catch_to_admin_forms'),
    path('catch_to_admin_num/<str:what>/<str:short_name>/', views.catch_to_admin_forms_num,
    name='catch_to_admin_forms_num'),
    path('catch_to_admin_shorts/<int:comp_pk>/', views.catch_to_admin_shorts,
    name='catch_to_admin_shorts'),
    path('get_discr_for_admin/<str:test_pk>/', views.get_discr_for_admin,
    name='get_discr_for_admin'),
    path('admin_change/ya/<str:test_pk>/', views.admin_change, name='admin_change'),
    path('admin_margin/<str:test_pk>/', views.admin_margin_exch, name='admin_margin_exch'),
    path('admin_special_price/<str:test_pk>/', views.admin_special_price,
    name='admin_special_price'),
    path('promotions_admin_edit/<int:comp_pk>/<int:prom_pk>/', views.promotions_admin_edit,
    name='promotions_admin_edit'),
    path('activate_comp/<int:comp_pk>/', views.activate_change_comp, name='activate_change_comp'),
    path('change_assembly_comp/<int:comp_pk>/', views.change_assembly, name='change_assembly'),
    path('change_comp_name/<int:comp_pk>/', views.change_comp_name, name='change_comp_name'),
    path('del_serv/<str:serv_pk>/', views.del_servise, name='del_servise'),
    path('stats_rules/<str:site>/<int:param>/<str:month>/<str:year>/',
    views.stats_rules, name='stats_rules'),
    path('plan_change/<str:site_>/<str:month_>/<str:year_>/',
    views.plan_change, name='plan_change'),
    path('gross_profit_change/<str:site_>/<str:month_>/<str:year_>/',
    views.gross_profit_change, name='gross_profit_change'),
    ]
