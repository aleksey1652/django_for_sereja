from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.utils.html import mark_safe

from .models import *
from cat.models import Computers
from .admin_filter import *

@admin.register(Assemblage)
class AssemblageAdmin(admin.ModelAdmin):
    search_fields = ['proc', 'gpu', 'ram',]
    list_display = ('get_name', 'groups', 'ver', 'it', 'hot', 'art',
    'tel', 'comp', 'versum_it', 'versum_hot', 'versum_art',
    'versum_tel', 'versum_com',)
    readonly_fields = ('date_ch',)
    #list_editable = ('is_published',) # для редактирования этого поля тут же
    prepopulated_fields = {"slug": ("name",)} # создаем/меняем name-создается/меняется и slug
    fields = ('name', 'groups', 'slug', 'date_ch', 'is_active', 'proc', 'gpu', 'ram',
    'ram_type', 'versum', 'itblok', 'hotline', 'artline','telemart', 'compx',
    'ver_price', 'it_price', 'hot_price', 'art_price','tel_price', 'com_price',
    'ver_it', 'ver_hot', 'ver_art','ver_tel', 'ver_com',)
    list_filter = (GroupsFilter, 'ram_type', 'date_ch', 'is_active',)
    date_hierarchy = 'date_ch'
    actions = ['set_active',]
    save_as = True
    save_on_top = True

    def get_name(self, object):
        return f'{str(object.proc)}-{str(object.gpu)}-{object.ram}-{object.ram_type}'

    get_name.short_description = "Имя"

    def set_active(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_rivals_active',
                                    kwargs={'rivals_pk': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    set_active.short_description = 'Установка Вкл/выкл массовая'

    def ver(self, object):
        return mark_safe(f'<span style="color: blue;">{object.ver_price}</span>')
    ver.short_description = "ver"

    def it(self, object):
        return mark_safe(f'<span style="color: #dc143c;">{object.it_price}</span>')
    it.short_description = "it"

    def hot(self, object):
        return mark_safe(f'<span style="color: #2f4f4f;">{object.hot_price}</span>')
    hot.short_description = "hot"

    def art(self, object):
        return mark_safe(f'<span style="color: #00bfff;">{object.art_price}</span>')
    art.short_description = "art"

    def tel(self, object):
        return mark_safe(f'<span style="color: #32cd32;">{object.tel_price}</span>')
    tel.short_description = "tel"

    def comp(self, object):
        return mark_safe(f'<span style="color: #ff8c00;">{object.com_price}</span>')
    comp.short_description = "comp"

    def versum_it(self, object):
        if isinstance(object.ver_it, float) and object.ver_it > 0:
            return mark_safe(
            f'<span style="background: red;color: white;">{object.ver_it}</span>')
        return mark_safe(f'<span style="color: #dc143c;">{object.ver_it}</span>')
    versum_it.short_description = "versum_it"

    def versum_hot(self, object):
        if isinstance(object.ver_hot, float) and object.ver_hot > 0:
            return mark_safe(
            f'<span style="background: red;color: white;">{object.ver_hot}</span>')
        return mark_safe(f'<span style="color: #2f4f4f;">{object.ver_hot}</span>')
    versum_hot.short_description = "versum_hot"

    def versum_art(self, object):
        if isinstance(object.ver_art, float) and object.ver_art > 0:
            return mark_safe(
            f'<span style="background: red;color: white;">{object.ver_art}</span>')
        return mark_safe(f'<span style="color: #00bfff;">{object.ver_art}</span>')
    versum_art.short_description = "versum_art"

    def versum_tel(self, object):
        if isinstance(object.ver_tel, float) and object.ver_tel > 0:
            return mark_safe(
            f'<span style="background: red;color: white;">{object.ver_tel}</span>')
        return mark_safe(f'<span style="color: #32cd32;">{object.ver_tel}</span>')
    versum_tel.short_description = "versum_tel"

    def versum_com(self, object):
        if isinstance(object.ver_com, float) and object.ver_com > 0:
            return mark_safe(
            f'<span style="background: red;color: white;">{object.ver_com}</span>')
        return mark_safe(f'<span style="color: #ff8c00;">{object.ver_com}</span>')
    versum_com.short_description = "versum_com"


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)} # создаем/меняем name-создается/меняемся и slug
    save_as = True
    save_on_top = True


@admin.register(Rentabilitys)
class RentabilitysAdmin(admin.ModelAdmin):
    list_display = ('rentability',)
