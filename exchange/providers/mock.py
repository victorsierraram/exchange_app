import random
from datetime import datetime
from .base import ExchangeRateProvider

class MockExchangeRateProvider(ExchangeRateProvider):
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        return round(random.uniform(0.8, 1.2), 6)
