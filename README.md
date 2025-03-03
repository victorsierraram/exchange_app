# MyCurrency: Currency Conversion Platform

## Overview

MyCurrency is a web platform built with Django that provides real-time currency conversion and historical exchange rate data. It supports multiple currency providers and offers a RESTful API for integration with frontend or mobile applications.

## Features

### 1. **Currency Conversion**
   - **Endpoint**: `/convert/` (POST)
   - **Parameters**:
     - `source_currency`: The currency code to convert from (e.g., "USD").
     - `amount`: The amount to convert.
     - `exchanged_currency`: The currency code to convert to (e.g., "EUR").
   - **Response**: Returns the converted amount based on the latest exchange rate.

### 2. **Historical Exchange Rates**
   - **Endpoint**: `/exchange-rates/` (GET)
   - **Parameters**:
     - `source_currency`: The currency code to fetch rates for.
     - `date_from`: The starting date for historical rates.
     - `date_to`: The end date for historical rates.
   - **Response**: Returns a list of exchange rates for the given date range.

### 3. **CRUD for Currencies**
   - **Endpoint**: `/currencies/` (GET, POST, PUT, DELETE)
   - Allows the creation, reading, updating, and deletion of currencies in the system.

### 4. **Exchange Rate Providers**
   - **Currency Providers**:
     - `CurrencyBeacon` (external provider).
     - `MockProvider` (simulated data for testing).
   - **Prioritization**: The platform supports a priority system for providers, allowing the selection of a default provider.
   - **Modularity**: New providers can be easily added to the system.

### 5. **Data Caching & Provider Fallback**
   - **Caching**: The platform stores exchange rates in the database for reuse.
   - **Fallback**: If a provider fails or doesn't return data, the system tries the next provider in the priority list.

### 6. **Asynchronous Data Fetching**
   - Uses **Celery** for asynchronous tasks to load historical data in the background.
   - The system fetches exchange rates for a range of dates using multiple providers.

## Setup

### 1. **Environment Setup**
   - Python 3.11
   - Django 4
   - Celery with Redis as the broker.
   - Install dependencies with `pip install -r requirements.txt`.

### 2. **Configuration**
   - Set the default exchange rate provider in the `settings.py` file.
   - Configure Celery to use a broker for background tasks.

### 3. **Run the App**
   - Start the Django server: `python manage.py runserver`.
   - Start the Celery worker: `celery -A config worker --loglevel=info`.

### 4. **Execute async task manually**
   - Populate db with task rates: `python manage.py shell_plus`.
   - Import task function: `from exchange.tasks import load_historical_data_task`.
   - Call it! : `load_historical_data_task.delay("CurrencyBeacon", "EUR", "USD", 30)`. You can use "mock" instead CurrencyBeacon to avoid requesting external service. 30 are number of days will be generated or requested.
   - You have to see the worker collecting rates and saving them into db.

## Example Usage

1. **Convert Currency**:
   - POST request to `/convert/` with `source_currency`, `amount`, and `exchanged_currency`.
   
2. **Get Historical Rates**:
   - GET request to `/exchange-rates/` with `source_currency`, `date_from`, and `date_to` as parameters.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
