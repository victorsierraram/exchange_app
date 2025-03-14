from celery import shared_task
import asyncio
from exchange.services.historical_data_loader import load_historical_data

from celery import shared_task
import asyncio

@shared_task
def load_historical_data_task(provider, source_currency, exchanged_currency, days=30):
    asyncio.run(load_historical_data(provider, source_currency, exchanged_currency, days))
    return f"Carga de datos históricos completada para {source_currency} -> {exchanged_currency}"


