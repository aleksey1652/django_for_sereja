from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .admin_filter import *

class Cooler_Inline(admin.StackedInline):
    model = Cooler_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0
#
@admin.register(Cooler_OTHER)
class CoolerAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorCooler, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        Cooler_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cooler_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cooler_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cooler_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

class CPU_Inline(admin.StackedInline):
    model = CPU_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(CPU_OTHER)
class CPUAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorCPU, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        CPU_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cpu_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cpu_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cpu_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class MB_Inline(admin.StackedInline):
    model = MB_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(MB_OTHER)
class MBAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorMB, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        MB_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'mb_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'mb_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'mb_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class RAM_Inline(admin.StackedInline):
    model = RAM_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(RAM_OTHER)
class RAMAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorRAM, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        RAM_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'ram_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'ram_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'ram_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class HDD_Inline(admin.StackedInline):
    model = HDD_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(HDD_OTHER)
class HDDAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorHDD, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        HDD_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'hdd_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'hdd_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'hdd_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class PSU_Inline(admin.StackedInline):
    model = PSU_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(PSU_OTHER)
class PSUAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorPSU, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        PSU_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'psu_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'psu_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'psu_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class GPU_Inline(admin.StackedInline):
    model = GPU_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(GPU_OTHER)
class GPUdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorGPU, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        GPU_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'gpu_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'gpu_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'gpu_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class FAN_Inline(admin.StackedInline):
    model = FAN_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(FAN_OTHER)
class FANAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorFAN, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        FAN_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'fan_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'fan_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'fan_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class CASE_Inline(admin.StackedInline):
    model = CASE_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(CASE_OTHER)
class CASEAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorCase, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        CASE_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'case_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'case_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'case_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class SSD_Inline(admin.StackedInline):
    model = SSD_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(SSD_OTHER)
class SSDAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorSSD, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        SSD_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'ssd_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'ssd_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'ssd_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class WiFi_Inline(admin.StackedInline):
    model = WiFi_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(WiFi_OTHER)
class WiFiAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorWiFi, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        WiFi_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'wifi_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'wifi_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'wifi_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Cables_Inline(admin.StackedInline):
    model = Cables_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Cables_OTHER)
class CablesAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorCables, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        Cables_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cables_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cables_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cables_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Soft_Inline(admin.StackedInline):
    model = Soft_OTHER
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Soft_OTHER)
class SoftAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = ('vendor', ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    list_display = (
    'name', 'get_sum_part_number', 'is_active', 'price_rent', 'get_price_rent_price_ua',
    'r_price', 'rrp_price', 'auto', 'price_ua', 'price_usd', 'provider',
    'hotline', 'delivery', 'creditoff',
    )
    list_editable = ('r_price', 'price_rent', 'auto')
    actions = ['change_rentability', 'change_pack_few', 'change_auto']
    autocomplete_fields = ['groups',]
    save_as = True
    save_on_top = True

    inlines = [
        Soft_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customs.css',),
        }
        js = ('admin/js/auto_saves.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'soft_other'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'soft_other'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'soft_other'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'
