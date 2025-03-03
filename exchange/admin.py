from django.contrib import admin
from .models import Currency, CurrencyExchangeRate

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')
    search_fields = ('code', 'name')

@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
    list_filter = ('valuation_date', 'source_currency', 'exchanged_currency')
    search_fields = ('source_currency__code', 'exchanged_currency__code')
