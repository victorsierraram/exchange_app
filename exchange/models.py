from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"

class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name="exchanges", on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)

    def __str__(self):
        return f"{self.source_currency.code} -> {self.exchanged_currency.code} on {self.valuation_date} at {self.rate_value}"
