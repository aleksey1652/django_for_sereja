"""

"""

from django.urls import path
from . import views
from . import tests

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
    path('renamegroup/<str:page>-<int:pc_ass>', tests.rename_group, name='rename_group'),
    path('addseries/<str:page>-<int:pc_ass>', tests.add_series, name='add_series'),
    path('renameseries/<str:page>', tests.rename_series, name='rename_series'),
    path('testgroup/<int:kind>', tests.test_group, name='test_group'),
    path('price_get_new_models/<str:prov>', tests.price_get_new_models, name='price_get_new_models'),
    path('price_get_tech_models/<str:prov>', tests.price_get_tech_models, name='price_get_tech_models'),
    path('test_price/<int:d>', views.test_price, name='test_price'),
    path('special_price/<int:pc_pk>', views.special_price, name='special_price'),
    path('test_assembly/<int:short_id>-<int:id_>-<int:pc_id>/', views.test_assembly,
    name='test_assembly'),
    path('forversum/<str:i>-<int:id>', views.forversum, name='forversum'),
    path('forversum_other/<str:kind_other>-<int:id_other>', views.forversum_other, name='forversum_other'),
    path('advanced_reserve/<int:page_id>-<str:price>-<int:grp>', views.pc_assembly_page_advanced, name='pc_assembly_page_advanced'),
    path('price_itblok/<int:id>', views.for_itblok, name='for_itblok'),
    path('prom/<str:site>-<int:prom_id>/', tests.promotion, name='promotion'),
    path('adv_comps_discr/<int:id>', views.adv_comps_discr, name='adv_comps_discr'),
    path('calc_comp/<int:comp_pk>/', views.calc_to_view, name='calc_to_view'),
    path('catch_to_calc_forms/<str:what>/<str:short_name>/', views.catch_to_calc_forms,
    name='catch_to_calc_forms'),
    path('start_to_calc/calc/<int:comp_pk>/', views.start_to_calc, name='start_to_calc'),
    path('edit_parts_pack/<str:comp_pack>/', views.edit_parts_pack, name='edit_parts_pack'),
    path('edit_parts_num/<str:comp_pack>/', views.edit_parts_num, name='edit_parts_num'),
    path('change_time_assembly/<str:comp_pack>/', views.change_time_assembly,
    name='change_time_assembly'),
    path('change_promotin_for_comps/<str:comp_pack>/', views.change_promotin_for_comps,
    name='change_promotin_for_comps'),

]
