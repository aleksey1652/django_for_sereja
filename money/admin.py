from django.contrib import admin
from .models import *
from django.db.models import Sum, Count
from django.contrib import messages
import re
from money.onec_transforms import get_dict_to_bids_advanced

#first_sborsik few_sborsik
class Goods_Inline(admin.StackedInline):
    model = Goods
    extra = 0

@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'site','status','date_ch', 'managers', 'display_goods')
    exclude = ('family', 'few_sborsik', 'first_sborsik')
    list_filter = ('status','date_ch', 'site', 'managers', 'istocnikZakaza', 'nds',  'sposobOplaty')
    search_fields = ['ID', 'managers__name']
    autocomplete_fields = ['managers']
    date_hierarchy = 'date_ch'

    inlines = [
        Goods_Inline,
    ]

@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'remontnik','sborsik','super', 'cash_rate')
    list_filter = ('is_active', 'remontnik','sborsik','super', 'site')
    #exclude = ('parts_full', 'providers')
    search_fields = ['name']
    #inlines = [BidsInline]

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('bids', 'kind', 'summa', 'amount', 'display_managers', 'discr')
    #exclude = ('software_bonus',)
    list_filter = ('kind','bids__date_ch')
    date_hierarchy = 'bids__date_ch'
    search_fields = ['bids__ID',]
    raw_id_fields = ["bids"]

@admin.register(Bids_advanced)
class Bids_advancedAdmin(admin.ModelAdmin):
    #list_display = ('ID', 'site','status','date_ch', 'managers', 'display_goods')
    list_filter = ('date_ch','managers', 'site', 'status', 'sposobOplaty', 'istocnikZakaza', 'nds')
    change_list_template = 'admin/test_change_list.html'
    date_hierarchy = 'date_ch'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            messages.error(request,f'by me: {response.context_data.items()}')
            return response

        """metrics = {
            'Total': Count('goods'),
            'Sum': Sum('goods__summa'),
        }

        response.context_data['summary'] = list(
            qs
            .values('ID')
            .annotate(**metrics)
            .order_by('date_ch')
        )"""

        summary = get_dict_to_bids_advanced(qs)

        response.context_data['summary'] = summary

        return response

@admin.register(Average_check)
class Average_checkAdmin(admin.ModelAdmin):
    list_filter = ('date', 'site')
    list_display = ('site', 'price', 'hand_check', 'plan_check', 'date',)
    date_hierarchy = 'date'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('kind', 'sloznostPK', 'summa', 'cash_rate',)
    exclude = ('managers',)

@admin.register(Statistics_service)
class Statistics_serviceAdmin(admin.ModelAdmin):
    list_display = ('managers', 'service', 'date', 'cash_rate_already',)
    exclude = ('family',)
    list_filter = ('date', 'service__kind', 'service__sloznostPK')
    date_hierarchy = 'date'
    #raw_id_fields = ["managers", "service"]

@admin.register(Gross_profit)
class Gross_profitAdmin(admin.ModelAdmin):
    #exclude = ('family',)
    list_display = ('site', 'date', 'amount', 'quantity', 'rentability', 'grossprofit',
    'amountcomponents', 'grossprofitcomponents', 'totalSales', 'totalProfit',
    'sumSales', 'sumProfit', 'quantity_total')
    list_filter = ('date', 'site')
    date_hierarchy = 'date'

class Expense_Inline(admin.StackedInline):
    model = Expense
    extra = 0

@admin.register(Expense_groups)
class Expense_groupsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    """inlines = [
        Expense_Inline,
    ]"""

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('discr', 'site', 'amount','summa', 'is_active', 'date')
    list_filter = ('date', 'site','expense_groups', 'is_active')
    search_fields = ['discr',]
    date_hierarchy = 'date'


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('site', 'date', 'plan', 'zero_plan', 'profit_plan', 'y_plan')
    list_filter = ('date',)
    date_hierarchy = 'date'

@admin.register(Ratios)
class RatiosAdmin(admin.ModelAdmin):
    list_display = ('tax_ratio', 'itblok_ratio', 'versum_ratio', 'date')

"""@admin.register(Koefficient)
class KoefficientAdmin(admin.ModelAdmin):
    list_display = ('date','hand')
    list_filter = ('date',)
    date_hierarchy = 'date'"""
