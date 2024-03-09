from django.contrib import admin
from .models import *
from descriptions.models import *
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .forms import Parts_short_se_Form
from .admin_filter import *
from django.utils.html import mark_safe
from django.utils.html import format_html_join
import json
#from django.contrib.postgres.forms.jsonb import JSONField

admin.site.site_title = 'VERSUM'
admin.site.site_header = 'VERSUM'

@admin.register(USD)
class USDAdmin(admin.ModelAdmin):
    list_display = ('usd', 'margin', 'date_ch')

@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ('who', 'date_ch')
    #exclude = ('class_computers', 'warranty_computers', 'url_computers', 'pc_assembly')
    list_filter = ('who', 'date_ch')
    search_fields = ['who',]
    fields = ('who', 'who_desc', 'items_prettified',)
    readonly_fields = ('items_prettified',)

    def items_prettified(self, instance):
        #json_str = json.dumps(instance.json_data, indent=2, ensure_ascii=False)
        try:
            list_ = eval(instance.json_data)
            _, _ = (list_[0]['name_parts'], list_[0]['partnumber_parts'])
        except:
            list_ = [{'name_parts':'пусто', 'partnumber_parts': 'пусто'},]
        #return json_str
        return format_html_join(
            mark_safe('<br>'),
            '<li>{} --- {}</li>',
            ((line['name_parts'], line['partnumber_parts']) for line in list_),
        ) or mark_safe("<span class='errors'>I can't determine this address.</span>")
    items_prettified.short_description = 'Инфо+'


@admin.register(Computers)
class ComputersAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_display = ('comp_name_plus', 'price_computers',
    'warranty_computers', 'class_computers',
    'pc_assembly', 'time_assembly_ru', 'is_active')
    #exclude = ('class_computers', 'warranty_computers', 'url_computers', 'pc_assembly')
    list_filter = (
    MEM_ListFilter, MEM_TypeFilter, GPU_ListFilter, AMDCPU_ListFilter,
    IntelCPU_ListFilter, 'is_active', 'pc_assembly__kind_assembly', SiteSeries
    )
    search_fields = ['name_computers','video_computers', 'proc_computers',
    'mem_computers', 'mb_computers', 'hdd_computers', 'cool_computers',
    'case_computers', 'ps_computers', 'vent_computers', 'wifi_computers', 'soft_computers',]
    change_form_template = 'admin/fieldset_my.html'#'admin/comp_details_admin.html'
    actions = ['change_advanced', 'set_margin', 'set_special_price',
    'edit_parts_pack_admin', 'edit_parts_num_admin',
    'change_time_assembly', 'change_promotin_for_pack',]
    readonly_fields = ('url_computers', 'class_computers', 'warranty_computers',
    'pc_assembly')

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term,
        )

        if not self.model.objects.filter(name_computers__icontains=search_term).exists():
            queryset = self.model.objects.filter(
            Q(video_computers__exact=search_term)|
            Q(proc_computers__exact=search_term) |Q (mem_computers__exact=search_term)|
            Q(mb_computers__exact=search_term) | Q(vent_computers__exact=search_term)|
            Q(hdd_computers__icontains=search_term) | Q(cool_computers__exact=search_term)|
            Q(case_computers__exact=search_term) | Q(ps_computers__exact=search_term)|
            Q(wifi_computers__exact=search_term) | Q(soft_computers__exact=search_term)
            )
            return queryset, may_have_duplicates

        return queryset, may_have_duplicates

    def get_advance(self, object_id):
        from cat.views_to_admin import get_comp_context, get_art_comp_context
        from load_form_providers.load_element import test_comp
        from cat.forms_admin_comps import Form_text_input

        form = Form_text_input()

        comp = Computers.objects.get(pk=object_id)
        test_ = test_comp(comp)
        if comp.pc_assembly.sites.name_sites == 'art':
            _, count_price, count_video_price = get_art_comp_context(object_id)
            try:
                count_price = round(float(count_price.price_computers))
            except:
                count_price = count_price.price_computers
            return (_, object_id, test_, comp, count_price, 'label')
        else:
            _, count_price = get_comp_context(object_id)
            return (_, object_id, test_, comp, count_price, form)

        #return (_, object_id, test_, comp, count_price)


    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['extra_data'] = self.get_advance(object_id)
        return super(ComputersAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def change_advanced(self, request, queryset):
        #admin_change from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_change',
                                    kwargs={'test_pk': ','.join(str(pk) for pk in selected) + ',Computers'}
                                    )
                                    )
    change_advanced.short_description = 'Опциональное редактирование'

    def set_margin(self, request, queryset):
        # admin_margin_exch from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_margin_exch',
                                    kwargs={'test_pk': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    set_margin.short_description = 'Установка наценки'

    def set_special_price(self, request, queryset):
        # admin_special_price from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_special_price',
                                    kwargs={'test_pk': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    set_special_price.short_description = 'Установка спец цены'

    def edit_parts_pack_admin(self, request, queryset):
        #edit_parts_pack from cat.calc_comp.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('edit_parts_pack',
                                    kwargs={'comp_pack': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    edit_parts_pack_admin.short_description = 'Массовая замена детали'

    def edit_parts_num_admin(self, request, queryset):
        #edit_parts_num from cat.calc_comp.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('edit_parts_num',
                                    kwargs={'comp_pack': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    edit_parts_num_admin.short_description = 'Замена кол вентиляторов'

    def change_time_assembly(self, request, queryset):
        #change_time_assembly from cat.calc_comp.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_time_assembly',
                                    kwargs={'comp_pack': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    change_time_assembly.short_description = 'Массовое изм срока сборки'

    def change_promotin_for_pack(self, request, queryset):
        # change_time_assembly from cat.calc_comp.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_promotin_for_comps',
                                    kwargs={'comp_pack': ','.join(str(pk) for pk in selected)}
                                    )
                                    )
    change_promotin_for_pack.short_description = 'Массовое добавление ярлыка'

    """def add_or_clear_filters(self, request, queryset):
        from cat.views_to_admin import add_or_clear_comp_code
        #test_queryset = queryset.update(kind='imb')
        #selected = queryset.values_list('pk', flat=True)
        add_or_clear_comp_code(queryset)
    add_or_clear_filters.short_description = 'Добавить/сделать неактивным фильтр для сравнений'"""

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    exclude = ('parts_full', 'providers')
    list_filter = ('item_price',)
    search_fields = ['article']
    actions = ['change_kind']

    def change_kind(self, request, queryset):
        # admin_test from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_test',
                                    kwargs={'test_pk': ','.join(str(pk) for pk in selected) + ',Articles'}
                                    )
                                    )
    change_kind.short_description = 'Изменить принадлежнось к группе данного артикля'

class Computers_AssemblyInline(admin.StackedInline):
    model = Computers
    fields = ('pc_assembly',)
    autocomplete_fields = ['pc_assembly']
    save_as = True
    extra = 0

@admin.register(Pc_assembly)
class Pc_assemblyAdmin(admin.ModelAdmin):
    #exclude = ('sites',)
    list_filter = ('sites', 'kind_assembly')
    search_fields = ['name_assembly', 'kind_assembly']
    actions = ['change_discr']
    #autocomplete_fields = ['computers']
    save_on_top = True

    inlines = [
        Computers_AssemblyInline,
    ]

    def change_discr(self, request, queryset):
        # admin_change from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_change',
                                    kwargs={'test_pk': ','.join(str(pk) for pk in selected) + ',Pc_assembly'}
                                    )
                                    )
    change_discr.short_description = 'Изменить описание серии'

@admin.register(Parts_full)
class Parts_fullAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_display = ('name_parts', 'partnumber_parts', 'providerprice_parts',
    'availability_parts', 'get_short', 'name_parts_main', 'remainder',)
    exclude = ('url_parts', 'item_price')
    list_filter = (PriceKindFilter, PriceProvFilter, PriceAvailFilter,
    ('remainder', admin.EmptyFieldListFilter))
    search_fields = ['name_parts', 'partnumber_parts']
    actions = ['change_kind']
    save_as = True
    save_on_top = True
    ordering = ('providerprice_parts',)

    def change_kind(self, request, queryset):
        # admin_test from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_test',
                                    kwargs={'test_pk': ','.join(str(pk) for pk in selected) + ',Parts_full'}
                                    )
                                    )
    change_kind.short_description = 'Изменить принадлежнось к группе данного злемента прайса'
    #change_kind.short_description = "Parts_full change kind"

@admin.register(Parts_short)
class Parts_shortAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    form = Parts_short_se_Form
    list_display = (
    'name_parts', 'in_comps', 'x_code', 'parts_full_price',
    'sklad_view', 'min_price', 'auto',
    'kind', 'itblok_versum_view', 'parts_full_view', 'get_providers',
    'description_view', 'special_price', 'config',
    )
    list_editable = ('x_code', 'min_price')
    list_filter = ('kind', ShortsKind2Filter, 'auto', ShortsIn_compsFilter,)
    #'hand',Parts_short_x_code_ListFilter
    search_fields = ['name_parts', 'x_code', 'partnumber_list']
    #autocomplete_fields = ['computer_shorts']
    actions = ['relate_to_parts_full', 'derelate_to_parts_full']
    autocomplete_fields = ['cpu_shorts', 'mb_shorts', 'ram_shorts', 'hdd_shorts',
    'ssd_shorts', 'psu_shorts', 'gpu_shorts', 'fan_shorts', 'case_shorts',
    'wifi_shorts', 'cables_shorts', 'soft_shorts', 'cooler_shorts',]
    #save_as = True
    save_on_top = True

    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',),
        }
        #js = ('admin/js/auto_save.js',)

    def relate_to_parts_full(self, request, queryset):
        # admin_test from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_test',
                                    kwargs={
                                    'test_pk': ','.join(str(pk) for pk in selected) + ',Parts_short'
                                    })
                                    )
    relate_to_parts_full.short_description = 'Привязать к детале из прайса'

    def derelate_to_parts_full(self, request, queryset):
        # admin_delete_relate from money.views.py
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_delete_relate',
                                    kwargs={
                                    'test_pk': ','.join(str(pk) for pk in selected) + ',Parts_short'
                                    })
                                    )
    derelate_to_parts_full.short_description = 'Отвязать деталь из прайса'

class ComputersInline(admin.StackedInline):
    model = Computers.promotion_set.through
    extra = 0
    save_as = True
    save_on_top = True
    #fields = ('name_computers',)
    #readonly_fields = ('name_computers',)
    #search_fields = ['promotion']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_filter = ('english_prom', 'prom',)
    list_display = ('prom', 'english_prom', 'display_computers',)
    fields = ('english_prom', 'prom', 'computers')
    autocomplete_fields = ['computers']
    save_on_top = True

    inlines = [
        ComputersInline,
    ]
"""
@admin.register(Computer_code)
class Computer_codeAdmin(admin.ModelAdmin):
    list_filter = ('code_is_active',)
    raw_id_fields = ('comp',)
    list_display = ('cpu_code', 'video_code', 'mem_code',)
    actions = ['art_upload_per_filter', 'art_stats_per_filter']

    def art_upload_per_filter(self, request, queryset):
        #from cat.views_to_admin import get_soup_art
        #from sereja.tasks import task_art_to_admin
        try:
            from sereja.tasks import task_art_to_admin
            #from sereja.celery import app
            #from cat.views_to_admin import get_soup_art
            #@app.task
            #def task_art_to_admin(url, queryset):
            #    get_soup_art(url, queryset)
            queryset_pk = tuple(queryset.values_list('pk',flat=True))
            task_art_to_admin.delay('https://artline.ua', queryset_pk)
        except:
            from cat.views_to_admin import get_soup_art
            get_soup_art('https://artline.ua', queryset_pk)
        #get_soup_art('https://artline.ua', queryset)
    art_upload_per_filter.short_description = 'Скачать с Artline'

    def art_stats_per_filter(self, request, queryset):
        from cat.views_to_admin import get_stats_art
        from django.shortcuts import render
        stats = get_stats_art(queryset)
        context = {
                    'art_list': stats[0],
                    'count_our_video': stats[1],
                    'queryset_comps': stats[2],
                    }

        #return HttpResponse(f'{stats}')
        return render(request, 'admin/fieldset_art_stats.html', context)

    art_stats_per_filter.short_description = 'Статистика с Artline'
"""

class Cooler_OTHERInline(admin.StackedInline):
    model = Cooler_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(Cooler)
class CoolerAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        Cooler_OTHERInline,
    ]


    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'cooler'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class CPU_OTHERInline(admin.StackedInline):
    model = CPU_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    exclude = ('cpu_streem_ukr', 'cpu_render_ukr')
    save_as = True
    save_on_top = True

    inlines = [
        CPU_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'cpu'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""


class MB_OTHERInline(admin.StackedInline):
    model = MB_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(MB)
class MBAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        MB_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'mb'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class RAM_OTHERInline(admin.StackedInline):
    model = RAM_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        RAM_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'ram'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class HDD_OTHERInline(admin.StackedInline):
    model = HDD_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(HDD)
class HDDAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        HDD_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'hdd'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class PSU_OTHERInline(admin.StackedInline):
    model = PSU_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(PSU)
class PSUAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        PSU_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'psu'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class GPU_OTHERInline(admin.StackedInline):
    model = GPU_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(GPU)
class GPUdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    exclude = ('gpu_3d_ukr', 'gpu_VR_ukr')
    save_as = True
    save_on_top = True

    inlines = [
        GPU_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'gpu'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class FAN_OTHERInline(admin.StackedInline):
    model = FAN_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(FAN)
class FANAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        FAN_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'fan'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class CASE_OTHERInline(admin.StackedInline):
    model = CASE_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(CASE)
class CASEAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        CASE_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'case'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

class SSD_OTHERInline(admin.StackedInline):
    model = SSD_OTHER
    extra = 0
    save_as = True
    save_on_top = True

@admin.register(SSD)
class SSDAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'root_other__is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

    inlines = [
        SSD_OTHERInline,
    ]

    """def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not queryset.exists() and search_term:
            from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
            from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
            from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

            art = search_term
            kind_ = 'ssd'
            dict_for_db = get_res_ecatalog(art, kind_)
            if dict_for_db:
                key_ = 'both'
                count_obj,obj_pk = eval(dict_kind_key[kind_])
            print(search_term)

        return queryset, use_distinct"""

@admin.register(WiFi)
class WiFiAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True

@admin.register(Cables)
class CablesAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'r_price', 'is_active', 'config')
    save_as = True
    save_on_top = True

@admin.register(Soft)
class SoftAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'config')
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active', 'config')
    save_as = True
    save_on_top = True
