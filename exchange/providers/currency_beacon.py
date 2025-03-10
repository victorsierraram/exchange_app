import requests
from datetime import datetime
from django.conf import settings
from .base import ExchangeRateProvider

class CurrencyBeaconProvider(ExchangeRateProvider):
    BASE_URL = "https://api.currencybeacon.com/v1"
    API_KEY = settings.CURRENCY_BEACON_API_KEY

    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        print("INSIDE CURRENCY BEACON EXCHANGE RATE PROVIDER")
        url = f"{self.BASE_URL}/convert"
        params = {
            "from": source_currency,
            "to": exchanged_currency,
            "date": valuation_date,
            "api_key": self.API_KEY
        }
        print(f"PREVIOUS RESPONSE wit PARAMS {params}")
        response = requests.get(url, params=params)
        print(f"RESPONSE: {response}")
        if response.status_code == 200:
            data = response.json()
            return data.get("value")
        return None
