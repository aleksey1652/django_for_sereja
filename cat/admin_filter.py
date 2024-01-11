from django.contrib import admin
from .models import *

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

    cpu_ = (('1200', '1200'), ('1500', '1500'), ('1600', '1600'), ('1800', '1800'),
    ('200', '200'), ('2100', '2100'), ('2200', '2200'), ('220G', '220G'),
    ('2400', '2400'), ('2600', '2600'), ('2700', '2700'), ('2990', '2990'),
    ('3000', '3000'), ('3100', '3100'), ('3200', '3200'), ('3300', '3300'),
    ('3350', '3350'), ('3400', '3400'), ('3500', '3500'), ('3600', '3600'),
    ('3700', '3700'), ('3800', '3800'), ('3900', '3900'), ('3950', '3950'),
    ('3960', '3960'), ('3970X', '3970X'), ('3990', '3990'), ('4100', '4100'),
    ('4300', '4300'), ('4500', '4500'), ('4600', '4600'), ('5500', '5500'),
    ('5600', '5600'), ('5700', '5700'), ('5750', '5750'), ('5800', '5800'),
    ('5900', '5900'), ('5950', '5950'), ('7600', '7600'), ('7700', '7700'),
    ('7800', '7800'),
    ('7900', '7900'), ('7950', '7950'), ('950', '950'), ('9600', '9600'),
     ('970', '970'))

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

    cpu_ = (('10100', '10100'), ('10105', '10105'), ('10400', '10400'),
    ('10500', '10500'), ('10600', '10600'), ('10700', '10700'),
    ('10850', '10850'), ('10900', '10900'), ('10940', '10940'),
    ('11400', '11400'), ('11600', '11600'), ('11700', '11700'),
    ('11900', '11900'), ('12100', '12100'), ('12400', '12400'),
    ('12600', '12600'), ('12700', '12700'), ('12900', '12900'),
    ('13100', '13100'), ('13400', '13400'), ('13500', '13500'), ('13600', '13600'),
    ('13700', '13700'), ('13900', '13900'), ('1800', '1800'),
    ('1900', '1900'), ('3250', '3250'), ('4160', '4160'),
    ('5420', '5420'), ('5600', '5600'), ('5905', '5905'),
    ('5925', '5925'), ('6400', '6400'), ('6405', '6405'),
    ('9100', '9100'), ('9400', '9400'), ('9600', '9600'),
    ('9700', '9700'), ('9900', '9900'))

    def lookups(self, request, model_admin):
        return self.cpu_

    def queryset(self, request, queryset):
        if self.value():
            cpu_type = self.value()
            return queryset.filter(
                proc_computers__icontains=cpu_type
                                    )
        return queryset
