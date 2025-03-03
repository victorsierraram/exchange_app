from datetime import datetime
from exchange.providers.provider_manager import ProviderManager
from asgiref.sync import sync_to_async

@sync_to_async
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider=None):
    provider_instance = ProviderManager.get_provider(provider)
    return provider_instance.get_exchange_rate(source_currency, exchanged_currency, valuation_date)
