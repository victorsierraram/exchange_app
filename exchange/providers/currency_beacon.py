import requests
from datetime import datetime
from django.conf import settings
from .base import ExchangeRateProvider

class CurrencyBeaconProvider(ExchangeRateProvider):
    BASE_URL = "https://api.currencybeacon.com/v1"
    API_KEY = settings.CURRENCY_BEACON_API_KEY

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        url = f"{self.BASE_URL}/convert"
        params = {
            "from": source_currency,
            "to": exchanged_currency,
            "date": valuation_date.strftime("%Y-%m-%d"),
            "api_key": self.API_KEY
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("value")
        return None
