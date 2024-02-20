from django.contrib import admin
from .models import *

class GroupsFilter(admin.SimpleListFilter):

    title = 'Группы'
    parameter_name = 'groups'
    template = "admin/filter_rivals.html"

    def lookups(self, request, model_admin):

        gr = Groups.objects.values_list('name', flat=True)
        group = [(group_name, group_name) for group_name in gr]

        return tuple(group)

    def queryset(self, request, queryset):
        if self.value():
            group = self.value()
            return queryset.filter(
                groups__name=group
                                    )
        return queryset
