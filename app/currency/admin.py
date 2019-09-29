from django.contrib import admin
from django.db.models import Count

from .models import (Currency, Rate)


class CurrencyFilter(admin.SimpleListFilter):
    title = 'currency'
    parameter_name = 'currency'

    def lookups(self, request, model_admin):
        result = Currency.objects.annotate(rates_count=Count('rates')).filter(rates_count__gt=0).values()
        return [(i['id'], '{} [{}]'.format(i['name'], i['rates_count'])) for i in result]

    def queryset(self, request, queryset):
        return queryset.filter(**self.used_parameters)

    def value(self):
        return super(CurrencyFilter, self).value()


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date')
    list_filter = (CurrencyFilter,)
    exclude = ('mts',)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
