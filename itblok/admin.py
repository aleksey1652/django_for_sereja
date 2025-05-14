from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.db.models import Sum, Count
from django.contrib import messages
from django.utils.html import mark_safe
from django.utils.html import format_html_join

import re

from .models import *
from .admin_filter import *


@admin.register(ItblokComputers)
class ItblokComputersAdmin(admin.ModelAdmin):
    #
    list_max_show_all = 1000
    change_form_template = 'admin/change_form_itblok.html'
    list_display = ('name_computers', 'is_active', 'price_parts',
    'price_special', 'rentability', 'procent_prom', 'price_prom',
    'price_main',)
    list_filter = (ItSeriesFilter, ItGrupsFilter, 'is_active',
    MEM_TypeFilter, MEM_ListFilter, GPU_ListFilter,
    AMDCPU_ListFilter, IntelCPU_ListFilter, LabelFilter)
    fields = ('is_active', 'name_computers', 'name_computers_ua', 'price_parts',
    'price_special', 'rentability', 'procent_prom', 'price_prom',
    'price_main', 'hend_input', 'cpu', 'cooler', 'mb', 'ram', 'gpu',
    'hdd', 'ssd', 'psu', 'case', 'fan', 'wifi', 'cables', 'soft',
    'mem_num_computers', 'vent_num_computers', 'warr_ua', 'warr_ru',
    'label', 'series', 'grups', 'items_prettified',)
    readonly_fields = ('items_prettified',)
    search_fields = ['name_computers','cpu__name_parts', 'cooler__name_parts',
    'mb__name_parts', 'ram__name_parts', 'gpu__name_parts',
    'hdd__name_parts', 'ssd__name_parts', 'psu__name_parts',
    'case__name_parts', 'fan__name_parts', 'wifi__name_parts',
    'cables__name_parts', 'soft__name_parts',
    'label', 'series__series_name', 'grups__group_name',]
    actions = ['set_margin', 'edit_parts_num_admin',
    'change_label', 'edit_parts_pack',]
    save_on_top = True
    save_as = True

    def get_search_results(self, request, queryset, search_term):
        # переопределяем search_fields как в Версуме (по точному названию деталей)
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term,
        )

        if not self.model.objects.filter(name_computers__icontains=search_term).exists():
            queryset = self.model.objects.filter(
            Q(cpu__name_parts__exact=search_term)|
            Q(cooler__name_parts__exact=search_term) |Q (mb__name_parts__exact=search_term)|
            Q(ram__name_parts__exact=search_term) | Q(gpu__name_parts__exact=search_term)|
            Q(hdd__name_parts__exact=search_term) | Q(ssd__name_parts__exact=search_term)|
            Q(psu__name_parts__exact=search_term) | Q(case__name_parts__exact=search_term)|
            Q(fan__name_parts__exact=search_term) | Q(wifi__name_parts__exact=search_term)|
            Q(cables__name_parts__exact=search_term) | Q(soft__name_parts__exact=search_term)
            )
            return queryset, may_have_duplicates

        return queryset, may_have_duplicates

    def items_prettified(self, instance):
        # для построчного вывода характеристик компа (деталь --- ее цена) из
        # поля description компа
        try:
            description_list = eval(instance.description)
        except:
            description_list = [{'name_parts': 'пусто', 'price': 0},]
        #
        return format_html_join(
            mark_safe('<br>'),
            '<li>{} --- {}</li>',
            ((line['name_parts'], line['price']) for line in description_list),
        ) or mark_safe("<span class='errors'>I can't determine this address.</span>")
    items_prettified.short_description = 'Описание+'

    def set_margin(self, request, queryset):
        # it_margin_exch from itblok.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('it_margin_exch',
                                    kwargs={'it_pk': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    set_margin.short_description = 'Установка наценки'

    def edit_parts_num_admin(self, request, queryset):
        #edit_it_num_fan from itblok.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('edit_it_num_fan',
                                    kwargs={'comp_pack': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    edit_parts_num_admin.short_description = 'Замена кол вентиляторов'

    def change_label(self, request, queryset):
        #
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_label',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    change_label.short_description = 'Массовое изм ярлыков'

    def edit_parts_pack(self, request, queryset):
        #edit_parts_pack from cat.calc_comp.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('itblok_edit_parts_pack',
                                    kwargs={'comp_pack': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    edit_parts_pack.short_description = 'Массовая замена детали'

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    # в ItblokComputers есть отдельно серии компа
    list_display = ('series_name',)
    list_filter = ('series_name',)
    search_fields = ['series_name',]


@admin.register(Grups)
class GrupsAdmin(admin.ModelAdmin):
    # в ItblokComputers есть отдельно группы компа
    list_display = ('group_name',)
    list_filter = ('group_name',)
    search_fields = ['group_name',]

"""
@admin.register(PackFilters)
class PackFiltersAdmin(admin.ModelAdmin):
    # для руч добавления фильтров процов, вид, памяти
    list_display = ('filter_name', 'filter_kind')
    list_filter = ('filter_name', 'filter_kind')
    search_fields = ['filter_name', 'filter_kind']
"""
