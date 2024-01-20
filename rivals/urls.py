"""
http://127.0.0.1:5222/admin/login/?next=admin/login&next2=admin
для GET запросов всегда ? ключ: значение (& ключ: значение и тд) в скобках необязат
в request.GET next - ключ, admin/login - значение; next2 - ключ и тд

"""

from django.urls import path, re_path
from django.views.decorators.cache import cache_page # для кеша вебстраниц
# (кэш) если на основе функций то над фун в views, над фун-ей: @cache_page(60)
# (кэш) есть возможность кеш-я тегов, например подходит для редко изм боковых нтмл(сайдбаров)
# base.html - там используем, убрал-малость глюк, смотри в ютубе 22 урок Селфеду
# (кэш) еще способ кэш-я АПИ низк уровня (пример в utls.py в DataMixin)
from . import views

#app_name = "versum"

urlpatterns = [
    path('test_assemblage/<slug:assm_slug>/', views.test_assemblage, name='test_assemblage'),
    path('test_groups/<slug:gr_slug>/', views.test_groups, name='test_groups'),
    path('admin_rivals_active/<str:rivals_pk>/', views.admin_rivals_active,
    name='admin_rivals_active'),
]
