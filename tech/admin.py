from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .admin_filter import *
from singleparts.admin_filter import ProvFilter, FullFilter, LabelFilter


class Monitors_Inline(admin.StackedInline):
    model = Monitors
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Monitors)
class MonitorsAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorMonitors, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    exclude = ('sc_o', )
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
        Monitors_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'monitors'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'monitors'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'monitors'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class KM_Inline(admin.StackedInline):
    model = KM
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(KM)
class KMAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorKM, ProvFilter, 'is_active', FullFilter,
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
        KM_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'km'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'km'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'km'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Keyboards_Inline(admin.StackedInline):
    model = Keyboards
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Keyboards)
class KeyboardsAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorKeyboards, ProvFilter, 'is_active', FullFilter,
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
        Keyboards_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'keyboards'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'keyboards'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'keyboards'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Mouses_Inline(admin.StackedInline):
    model = Mouses
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Mouses)
class MousesAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorMouses, ProvFilter, 'is_active', FullFilter,
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
        Mouses_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'mouses'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'mouses'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'mouses'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Pads_Inline(admin.StackedInline):
    model = Pads
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Pads)
class PadsAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorPads, ProvFilter, 'is_active', FullFilter,
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
        Pads_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'pads'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'pads'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'pads'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Headsets_Inline(admin.StackedInline):
    model = Headsets
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Headsets)
class HeadsetsAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorHeadsets, ProvFilter, 'is_active', FullFilter,
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
        Headsets_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'headsets'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'headsets'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'headsets'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Webcams_Inline(admin.StackedInline):
    model = Webcams
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Webcams)
class WebcamsAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorWebcams, ProvFilter, 'is_active', FullFilter,
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
        Webcams_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'webcams'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'webcams'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'webcams'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class WiFis_Inline(admin.StackedInline):
    model = WiFis
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(WiFis)
class WiFisAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorWiFis, ProvFilter, 'is_active', FullFilter,
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
        WiFis_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'wifis'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'wifis'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'wifis'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Acoustics_Inline(admin.StackedInline):
    model = Acoustics
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Acoustics)
class AcousticsAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorAcoustics, ProvFilter, 'is_active', FullFilter,
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
        Acoustics_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'acoustics'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'acoustics'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'acoustics'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Tables_Inline(admin.StackedInline):
    model = Tables
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Tables)
class TablesAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorTables, ProvFilter, 'is_active', FullFilter,
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
        Tables_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'tables'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'tables'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'tables'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Chairs_Inline(admin.StackedInline):
    model = Chairs
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Chairs)
class ChairsAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorChairs, ProvFilter, 'is_active', FullFilter,
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
        Chairs_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'chairs'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'chairs'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'chairs'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Accessories_Inline(admin.StackedInline):
    model = Accessories
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Accessories)
class AccessoriesAdmin(admin.ModelAdmin):
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
        Accessories_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'accessories'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'accessories'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'accessories'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Cabelsplus_Inline(admin.StackedInline):
    model = Cabelsplus
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Cabelsplus)
class CabelsplusAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorCabelsplus, ProvFilter, 'is_active', FullFilter,
    TechFilter, 'auto', 'hotline', 'creditoff', LabelFilter)
    search_fields = ['part_number', 'name']
    exclude = ('cab_col_ua', 'cab_col_ru', 'cab_col_u', 'cab_col_r')
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
        Cabelsplus_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cabelsplus'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cabelsplus'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'cabelsplus'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Filters_Inline(admin.StackedInline):
    model = Filters
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Filters)
class FiltersAdmin(admin.ModelAdmin):
    list_max_show_all = 1000
    list_filter = (VendorFilters, ProvFilter, 'is_active', FullFilter,
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
        Filters_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'filters'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'filters'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'filters'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'

class Others_Inline(admin.StackedInline):
    model = Others
    fields = ('part_number', 'price_usd')
    save_as = True
    extra = 0

@admin.register(Others)
class OthersAdmin(admin.ModelAdmin):
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
        Others_Inline,
    ]

    class Media:
        css = {
            'all': ('admin/css/admin_customss.css',),
        }
        js = ('admin/js/auto_savess.js',)

    def get_rentability(self, object):
        return f'{str(object.price_rent)}({str(object.rentability)})'

    get_rentability.short_description = "Цена с наценкой"

    def change_rentability(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_rentability_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'others'}
                                    )
                                    )
    change_rentability.short_description = 'Массовое изм наценки'

    def change_auto(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_auto_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'others'}
                                    )
                                    )
    change_auto.short_description = 'Массовое изм ручной цены'

    def change_pack_few(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('change_few_things_obj_tech',
                                    kwargs={'obj_pack': ','.join(str(pk) for pk in selected),
                                    'obj_model': 'others'}
                                    )
                                    )
    change_pack_few.short_description = 'Массовое изм hotline_label_delivery'
