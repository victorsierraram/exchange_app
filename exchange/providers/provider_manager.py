from django.conf import settings
from .currency_beacon import CurrencyBeaconProvider
from .mock import MockExchangeRateProvider

class ProviderManager:
    
    PROVIDERS = {
        "currency_beacon": CurrencyBeaconProvider(),
        "mock": MockExchangeRateProvider(),
    }

    @classmethod
    def get_provider(cls, provider_name=None):
        if provider_name and provider_name in cls.PROVIDERS:
            return cls.PROVIDERS[provider_name]
        return cls.PROVIDERS.get(settings.DEFAULT_EXCHANGE_PROVIDER, cls.PROVIDERS["currency_beacon"])
