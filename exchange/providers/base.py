from abc import ABC, abstractmethod

class ExchangeRateProvider(ABC):

    @abstractmethod
    def get_exchange_rate(self, source_currency, exchanged_currency, valuation_date):
        pass