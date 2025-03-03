import asyncio
import datetime
from asgiref.sync import sync_to_async
from exchange.models import Currency, CurrencyExchangeRate
from exchange.services.exchange_service import get_currency_by_code
from exchange.utils import get_exchange_rate_data

async def load_historical_data(provider, source_currency_code, exchanged_currency_code, days):
    source_currency = await get_currency_by_code(source_currency_code)
    exchanged_currency = await get_currency_by_code(exchanged_currency_code)

    if not source_currency or not exchanged_currency:
        print(f"Currency not found: {source_currency_code} o {exchanged_currency_code}")
        return

    today = datetime.date.today()
    date_list = [today - datetime.timedelta(days=i) for i in range(days)]

    tasks = [fetch_and_store_rate(provider, source_currency, exchanged_currency, date) for date in date_list]
    await asyncio.gather(*tasks)

async def fetch_and_store_rate(provider, source_currency, exchanged_currency, valuation_date):
    rate_value = await get_exchange_rate_data(provider, source_currency.code, exchanged_currency.code, valuation_date)
    
    if rate_value:
        await update_or_create_rate(source_currency, exchanged_currency, valuation_date, rate_value)
        print(f"SAVED: {valuation_date} {source_currency.code}/{exchanged_currency.code} = {rate_value}")
    else:
        print(f"Couldn't be saved {valuation_date} ({provider.__class__.__name__})")

@sync_to_async
def update_or_create_rate(source_currency, exchanged_currency, valuation_date, rate_value):
    CurrencyExchangeRate.objects.update_or_create(
        source_currency=source_currency,
        exchanged_currency=exchanged_currency,
        valuation_date=valuation_date,
        defaults={'rate_value': rate_value}
    )

