from django.contrib import admin
from .models import *

from django.db.models import Q
#

class LabelFilter(admin.SimpleListFilter):
    #

    title = 'Ярлыки'
    parameter_name = 'label'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):

        return (
            ('пусто', 'пусто'),
            ('заполнено', 'заполнено'),
            ('new', 'new'),
            ('exclusive', 'exclusive'),
            ('hit', 'hit'),
            ('recommend', 'recommend'),
            ('sale', 'sale'),
            ('choice', 'choice'),
            ('offer', 'offer'),
            ('best_price_ever', 'best_price_ever'),
        )

    def queryset(self, request, queryset):
        if self.value() and self.value() == 'пусто':
            return queryset.filter(
                label__isnull=True
                                    )
        if self.value() and self.value() == 'заполнено':
            return queryset.filter(
                label__isnull=False
                                    )
        elif self.value() and self.value() not in ('пусто', 'заполнено'):
            return queryset.filter(
                label__icontains=self.value()
                                    )

        return queryset

class ItSeriesFilter(admin.SimpleListFilter):

    title = 'Серии'
    parameter_name = 'series_name'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        assembly = set(Series.objects.values_list('series_name', flat=True))
        return sorted([(asm, asm) for asm in assembly])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
            series__series_name=self.value()
            )

class ItGrupsFilter(admin.SimpleListFilter):

    title = 'Группы'
    parameter_name = 'group_name'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        assembly = set(Grups.objects.values_list('group_name', flat=True))
        return sorted([(asm, asm) for asm in assembly if asm])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
            grups__group_name=self.value()
            )

#
class MEM_TypeFilter(admin.SimpleListFilter):

    title = 'Тип_ОЗУ'
    parameter_name = 'ram'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):
        return (
            ('ddr3', 'ddr3'),
            ('ddr4', 'ddr4'),
            ('ddr5', 'ddr5'),
        )

    def queryset(self, request, queryset):
        if self.value():
            mem_size_type = self.value()
            return queryset.filter(
                ram__name_parts__icontains=mem_size_type
                                    )
        return queryset

class MEM_ListFilter(admin.SimpleListFilter):

    title = 'Обьем_ОЗУ'
    parameter_name = 'ram'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):
        return (
            ('8Gb', '8Gb'),
            ('16Gb', '16Gb'),
            ('32Gb', '32Gb'),
            ('64Gb', '64Gb'),
        )

    def queryset(self, request, queryset):
        if self.value():
            mem_size_type = self.value()
            return queryset.filter(
                ram__name_parts__icontains=mem_size_type
                                    )
        return queryset

class GPU_ListFilter(admin.SimpleListFilter):

    title = 'Видеокарты'
    parameter_name = 'gpu'
    template = "admin/filter_admin.html"

    video_ = (('1030', '1030'), ('1050', '1050'), ('1630', '1630'),
    ('1650', '1650'), ('1660', '1660'),
    ('3050', '3050'), ('3060', '3060'), ('3070', '3070'), ('3080', '3080'),
    ('3090', '3090'), ('4060', '4060'), ('4070', '4070'), ('4080', '4080'),
    ('4090', '4090'), ('550', '550'), ('560', '560'),
    ('5070', '5070'), ('5080', '5080'), ('5090', '5090'),
    ('6400', '6400'), ('6500', '6500'), ('6600', '6600'),
    ('6700', '6700'), ('6800', '6800'),
    ('7600', '7600'), ('7700', '7700'), ('7800', '7800'),('7900', '7900'),
    ('710', '710'), ('730', '730'), ('graphics', 'graphics'), ('vega', 'vega'))

    def lookups(self, request, model_admin):
        return self.video_

    def queryset(self, request, queryset):
        if self.value():
            video_type = self.value()
            return queryset.filter(
                gpu__name_parts__icontains=video_type
                                    )
        return queryset


class AMDCPU_ListFilter(admin.SimpleListFilter):

    title = 'AMDCPU'
    parameter_name = 'cpu'
    template = "admin/filter_admin.html"

    cpu_ = (
    ('1200', '1200'), ('1600', '1600'),
    ('2100', '2100'), ('2200', '2200'), ('2400', '2400'), ('2600', '2600'),
    ('3200', '3200'), ('3400', '3400'), ('3600', '3600'), ('3700', '3700'),
    ('4100', '4100'), ('4300', '4300'),
    ('4500', '4500'), ('4600', '4600'), ('5500', '5500'),
    ('5600', '5600'), ('5700', '5700'), ('5800', '5800'),
    ('5900', '5900'), ('5950', '5950'), ('7500', '7500'),
    ('7600', '7600'), ('7700', '7700'), ('7800', '7800'),
    ('7900', '7900'), ('7950', '7950'),
    ('8500', '8500'), ('8600', '8600'),
    ('9600', '9600'), ('9700', '9700'), ('9800', '9800'),
    ('9900', '9900'), ('9950', '9950'),
    )

    def lookups(self, request, model_admin):
        return self.cpu_

    def queryset(self, request, queryset):
        if self.value():
            cpu_type = self.value()
            return queryset.filter(
                cpu__name_parts__icontains=cpu_type
                                    )
        return queryset

class IntelCPU_ListFilter(admin.SimpleListFilter):

    title = 'IntelCPU'
    parameter_name = 'cpu'
    template = "admin/filter_admin.html"

    cpu_ = (
    ('10100', '10100'), ('10105', '10105'), ('10400', '10400'),
    ('11400', '11400'),
    ('12100', '12100'), ('12400', '12400'), ('12500', '12500'),
    ('12600', '12600'), ('12700', '12700'), ('12900', '12900'),
    ('13100', '13100'), ('13400', '13400'), ('13500', '13500'),
    ('13600', '13600'), ('13700', '13700'), ('13900', '13900'),
    ('14100', '14100'), ('14400', '14400'), ('14500', '14500'),
    ('14600', '14600'), ('14700', '14700'), ('14900', '14900'),
    )

    def lookups(self, request, model_admin):
        return self.cpu_

    def queryset(self, request, queryset):
        if self.value():
            cpu_type = self.value()
            return queryset.filter(
                cpu__name_parts__icontains=cpu_type
                                    )
        return queryset
