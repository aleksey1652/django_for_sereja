from django.contrib import admin
from .models import *

from django.db.models import Q
#
class PriceProvFilter(admin.SimpleListFilter):

    title = 'Пост'
    parameter_name = 'providers'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):
        return (
            ('dc', 'dc'),
            ('itlink', 'itlink'),
            ('asbis', 'asbis'),
            ('elko', 'elko'),
            ('mti', 'mti'),
            ('brain', 'brain'),
            ('edg', 'edg'),
            ('erc', 'erc'),
            ('be', 'be'),
            ('dw', 'dw'),
            ('-', '-'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                providers__name_provider=self.value()
                                    )
        return queryset.filter(
            providers__name_provider='-'
                                )

class SiteSeries(admin.SimpleListFilter):

    title = 'Группы'
    parameter_name = 'name_assembly'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        assembly = set(Pc_assembly.objects.values_list('name_assembly', flat=True))
        return sorted([(asm, asm) for asm in assembly])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
            pc_assembly__name_assembly=self.value()
            )

class PriceKindFilter(admin.SimpleListFilter):

    title = 'Вид'
    parameter_name = 'kind'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):
        return (
            ('cool', 'cool'),
            ('imb', 'imb'),
            ('amb', 'amb'),
            ('case', 'case'),
            ('ssd', 'ssd'),
            ('hdd', 'hdd'),
            ('aproc', 'aproc'),
            ('iproc', 'iproc'),
            ('video', 'video'),
            ('ps', 'ps'),
            ('mem', 'mem'),
            ('vent', 'vent'),
            ('mon', 'mon'),
            ('wifi', 'wifi'),
            ('km', 'km'),
            ('soft', 'soft'),
            ('cables', 'cables'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                kind=self.value()
                                    )
        return queryset

class PriceAvailFilter(admin.SimpleListFilter):

    title = 'Наличие'
    parameter_name = 'availability_parts'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
            ('q', 'q'),
            ('hand', 'hand'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                availability_parts=self.value()
                                    )
        return queryset.filter(
            availability_parts='yes'
                                )

class ShortsKind2Filter(admin.SimpleListFilter):

    title = 'Вкл/выкл'
    parameter_name = 'kind2'
    template = "admin/filter_admin.html"


    def lookups(self, request, model_admin):
        return (
            ('Нет', 'Нет'),
            ('Да', 'Да'),
        )

    def queryset(self, request, queryset):

        ValuesDict = {
                    'Нет': True,
                    'Да': False
                    }

        if self.value():
            return queryset.filter(
                kind2=ValuesDict[self.value()]
                                    )
        return queryset

class ShortsIn_compsFilter(admin.SimpleListFilter):

    title = 'В_сборке'
    parameter_name = 'in_comps'
    template = "admin/filter_admin.html"


    def lookups(self, request, model_admin):
        return (
            ('Да', 'Да'),
            ('Нет', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value():
            if self.value() == 'Да':
                return queryset.filter(
                                        Q(in_comps=True)|
                                        Q(computer_shorts__isnull=False)
                )
            else:
                return queryset.filter(
                                        computer_shorts__isnull=True,
                                        in_comps=False
                )
        return queryset

class MEM_TypeFilter(admin.SimpleListFilter):

    title = 'Тип ОЗУ'
    parameter_name = 'mem_computers'
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
                mem_computers__icontains=mem_size_type
                                    )
        return queryset

class MEM_ListFilter(admin.SimpleListFilter):

    title = 'Обьем ОЗУ'
    parameter_name = 'mem_computers'
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
                mem_computers__icontains=mem_size_type
                                    )
        return queryset

class GPU_ListFilter(admin.SimpleListFilter):

    title = 'Видеокарты'
    parameter_name = 'video_computers'
    template = "admin/filter_admin.html"

    video_ = (('1030', '1030'), ('1050', '1050'), ('1060', '1060'), ('1630', '1630'),
    ('1650', '1650'), ('1660', '1660'), ('2060', '2060'), ('2080', '2080'),
    ('3050', '3050'), ('3060', '3060'), ('3070', '3070'), ('3080', '3080'),
    ('3090', '3090'), ('4060', '4060'), ('4070', '4070'), ('4080', '4080'), ('4090', '4090'),
    ('550', '550'), ('5500', '5500'), ('560', '560'), ('5600', '5600'),
    ('570', '570'), ('5700', '5700'), ('580', '580'), ('6400', '6400'),
    ('6500', '6500'), ('6600', '6600'), ('6650', '6650'), ('6700', '6700'),
    ('6750', '6750'), ('6800', '6800'), ('6900', '6900'), ('6950', '6950'),
    ('7600', '7600'), ('7900', '7900'),
    ('710', '710'), ('730', '730'), ('graphics', 'graphics'), ('vega', 'vega'))

    def lookups(self, request, model_admin):
        return self.video_

    def queryset(self, request, queryset):
        if self.value():
            video_type = self.value()
            return queryset.filter(
                video_computers__icontains=video_type
                                    )
        return queryset

class AMDCPU_ListFilter(admin.SimpleListFilter):

    title = 'AMDCPU'
    parameter_name = 'proc_computers'
    template = "admin/filter_admin.html"

    cpu_ = (
    ('1200', '1200'),
    ('2600', '2600'),
    ('3200', '3200'),
    ('3600', '3600'),
    ('4100', '4100'),
    ('4500', '4500'), ('4600', '4600'), ('5500', '5500'),
    ('5600', '5600'), ('5700', '5700'), ('5800', '5800'),
    ('5900', '5900'), ('5950', '5950'), ('7500', '7500'),
    ('7600', '7600'), ('7700', '7700'), ('7800', '7800'),
    ('7900', '7900'), ('7950', '7950'),
     )

    def lookups(self, request, model_admin):
        return self.cpu_

    def queryset(self, request, queryset):
        if self.value():
            cpu_type = self.value()
            return queryset.filter(
                proc_computers__icontains=cpu_type
                                    )
        return queryset

class IntelCPU_ListFilter(admin.SimpleListFilter):

    title = 'IntelCPU'
    parameter_name = 'proc_computers'
    template = "admin/filter_admin.html"

    cpu_ = (
    ('10100', '10100'), ('10105', '10105'), ('10400', '10400'),
    ('10500', '10500'), ('10600', '10600'), ('10700', '10700'),
    ('10900', '10900'),
    ('11400', '11400'), ('11600', '11600'), ('11700', '11700'),
    ('11900', '11900'), ('12100', '12100'), ('12400', '12400'),
    ('12600', '12600'), ('12700', '12700'), ('12900', '12900'),
    ('13100', '13100'), ('13400', '13400'), ('13500', '13500'),
    ('13600', '13600'), ('13700', '13700'), ('13900', '13900'),
    ('14100', '14100'), ('14400', '14400'), ('14500', '14500'),
    ('14600', '14600'), ('14700', '14700'), ('14900', '14900'),
    ('6400', '6400'), ('6405', '6405'),
    )

    def lookups(self, request, model_admin):
        return self.cpu_

    def queryset(self, request, queryset):
        if self.value():
            cpu_type = self.value()
            return queryset.filter(
                proc_computers__icontains=cpu_type
                                    )
        return queryset
