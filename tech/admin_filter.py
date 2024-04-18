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

class VendorWiFis(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(WiFis.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorWebcams(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Webcams.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorHeadsets(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Headsets.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorCabelsplus(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Cabelsplus.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorPads(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Pads.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorKeyboards(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Keyboards.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorKM(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(KM.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorMouses(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Mouses.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorMonitors(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Monitors.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorAcoustics(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Acoustics.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorTables(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Tables.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorChairs(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Chairs.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())

class VendorFilters(admin.SimpleListFilter):

    title = 'vendor'
    parameter_name = 'vendor'
    template = 'admin/filter_admin.html'

    def lookups(self, request, model_admin):
        case = set(Filters.objects.values_list('vendor', flat=True))
        return [(vendor, vendor) for vendor in case]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor=self.value())
