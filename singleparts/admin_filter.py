from django.contrib import admin
from .models import *

class TechFilter(admin.SimpleListFilter):

    title = 'Дубли'
    parameter_name = 'mem_computers'
    template = "admin/filter_admin_dubli.html"

    def lookups(self, request, model_admin):
        return (
            ('Дубли', 'Дубли'),
        )

    def queryset(self, request, queryset):
        if self.value() and self.value() == 'Дубли':
            return queryset.filter(
                groups__isnull=False
                                    )
        return queryset.filter(
            groups__isnull=True
                                )

class LabelFilter(admin.SimpleListFilter):

    title = 'Label'
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
                label=self.value()
                                    )
        #elif self.value() and self.value() not in ('пусто', 'пусто'):
        #    return queryset.filter(label=self.value())
        return queryset

class FullFilter(admin.SimpleListFilter):

    title = 'Заполнен'
    parameter_name = 'full'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):
        return (
            ('Да', 'Да'),
            ('Нет', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() and self.value() == 'Да':
            return queryset.filter(full=True)
        elif self.value() and self.value() == 'Нет':
            return queryset.filter(full=False)
        return queryset

class ProvFilter(admin.SimpleListFilter):

    title = 'provider'
    parameter_name = 'provider'
    template = "admin/filter_admin.html"

    def lookups(self, request, model_admin):
        return (
            ('нет', 'нет'),
            ('склад', 'склад'),
            ('dc', 'dc'),
            ('itlink', 'itlink'),
            ('asbis', 'asbis'),
            ('elko', 'elko'),
            ('mti', 'mti'),
            ('brain', 'brain'),
            ('edg', 'edg'),
            ('erc', 'erc'),
            ('eletek', 'eletek'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(provider=self.value())

class VendorCase(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(CASE_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorSSD(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(SSD_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorCooler(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Cooler_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorCPU(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(CPU_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorMB(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(MB_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorRAM(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(RAM_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorHDD(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(HDD_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorPSU(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(PSU_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorGPU(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(GPU_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorFAN(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(FAN_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorWiFi(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(WiFi_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorCables(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Cables_OTHER.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())
