from asgiref.sync import sync_to_async
from exchange.models import Currency, CurrencyExchangeRate
from django.utils.dateparse import parse_date

def get_all_currencies():
    return Currency.objects.all()

def get_currency_by_id(currency_id):
    try:
        return Currency.objects.get(id=currency_id)
    except Currency.DoesNotExist:
        return None
    
def get_exchange_rates(source_currency, date_from=None, date_to=None):
    exchange_rates = CurrencyExchangeRate.objects.filter(source_currency=source_currency)
    
    if date_from:
        exchange_rates = exchange_rates.filter(valuation_date__gte=parse_date(date_from))
    if date_to:
        exchange_rates = exchange_rates.filter(valuation_date__lte=parse_date(date_to))
    return exchange_rates

def get_latest_exchange_rate(source_currency, exchanged_currency):
    return CurrencyExchangeRate.objects.filter(
        source_currency=source_currency,
        exchanged_currency=exchanged_currency
    ).order_by('-valuation_date').first()

@sync_to_async
def get_currency_by_code(currency_code):
    return Currency.objects.filter(code=currency_code).first()
