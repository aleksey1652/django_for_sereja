from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from .models import *
from django.db.models import Sum, Count
from django.contrib import messages
import re

@admin.register(Mark_computers)
class Mark_computersAdmin(admin.ModelAdmin):
    #form = Parts_short_se_Forms
    list_display = ('name_computers', 'price_computers', 'category', 'is_active')
    list_filter = ('category', 'is_active',)
    search_fields = ['name_computers',]
    save_on_top = True
    actions = ['rentability_chg',]

    def rentability_chg(self, request, queryset):
        #test_queryset = queryset.update(kind='imb')
        selected = queryset.values_list('pk', flat=True)

        return  HttpResponseRedirect(
                                    reverse('admin_rentability_chg',
                                    kwargs={
                                    'test_pk': ','.join(str(pk) for pk in selected)
                                    })
                                    )
    rentability_chg.short_description = 'Изменить наценку'

class Computers_AssemblyInline(admin.StackedInline):
    model = Mark_computers
    #exclude = ('category',)
    save_as = True
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('kind_assembly',)

    inlines = [
        Computers_AssemblyInline,
    ]

@admin.register(Mark_short)
class Mark_shortAdmin(admin.ModelAdmin):
    #form = Parts_short_se_Form
    list_display = ('name_parts', 'x_code', 'kind', 'trade_in',
    'trade_in_price', 'only_comp', 'kind2')
    list_filter = ('kind', 'kind2', 'trade_in', 'only_comp',)
    search_fields = ['name_parts',]
    #autocomplete_fields = ['computer_shorts']
    #actions = ['relate_to_parts_full']
    save_as = True
    save_on_top = True

@admin.register(Cooler)
class CoolerAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    exclude = ('depend_to', 'depend_to_type')
    save_as = True
    save_on_top = True


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    exclude = ('depend_from', 'depend_from_type')
    save_as = True
    save_on_top = True


@admin.register(MB)
class MBAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    exclude = ('main_category', 'depend_to', 'depend_to_type',
    'depend_from', 'depend_from_type')
    save_as = True
    save_on_top = True


@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    exclude = ('depend_to', 'depend_to_type',
    'depend_from', 'depend_from_type')
    save_as = True
    save_on_top = True


@admin.register(HDD)
class HDDAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    save_as = True
    save_on_top = True


@admin.register(PSU)
class PSUAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    save_as = True
    save_on_top = True


@admin.register(GPU)
class GPUdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    exclude = ('depend_to', 'depend_to_type', 'main_category')
    save_as = True
    save_on_top = True


@admin.register(FAN)
class FANAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    save_as = True
    save_on_top = True


@admin.register(CASE)
class CASEAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    exclude = ('depend_to', 'depend_to_type')
    save_as = True
    save_on_top = True


@admin.register(SSD)
class SSDAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    save_as = True
    save_on_top = True


@admin.register(WiFi)
class WiFiAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    save_as = True
    save_on_top = True

@admin.register(Cables)
class CablesAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'r_price', 'is_active')
    save_as = True
    save_on_top = True

@admin.register(Soft)
class SoftAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ['part_number', 'name']
    list_display = ('name', 'part_number', 'price', 'is_active')
    save_as = True
    save_on_top = True
