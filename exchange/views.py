from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from exchange.models import Currency
from .serializers import CurrencySerializer, CurrencyExchangeRateSerializer
from .services.exchange_service import get_all_currencies, get_currency_by_id, get_exchange_rates, get_latest_exchange_rate

class CurrencyListView(APIView):
    def get(self, request):
        currencies = get_all_currencies()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)

class CurrencyExchangeRateListView(APIView):
    def get(self, request):
        source_currency_code = request.query_params.get('source_currency', None)
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)

        if not source_currency_code:
            return Response({"error": "source_currency parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        source_currency = Currency.objects.filter(code=source_currency_code).first()
        if not source_currency:
            return Response({"error": "Source currency not found."}, status=status.HTTP_404_NOT_FOUND)

        exchange_rates = get_exchange_rates(source_currency, date_from, date_to)
        
        serializer = CurrencyExchangeRateSerializer(exchange_rates, many=True)
        return Response(serializer.data)

class CurrencyExchangeRateConvertView(APIView):
    def post(self, request):
        source_currency_code = request.data.get('source_currency', None)
        exchanged_currency_code = request.data.get('exchanged_currency', None)
        amount = request.data.get('amount', None)

        if not all([source_currency_code, exchanged_currency_code, amount]):
            return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        source_currency = Currency.objects.filter(code=source_currency_code).first()
        exchanged_currency = Currency.objects.filter(code=exchanged_currency_code).first()

        if not source_currency or not exchanged_currency:
            return Response({"error": "One or both currencies not found."}, status=status.HTTP_404_NOT_FOUND)

        exchange_rate = get_latest_exchange_rate(source_currency, exchanged_currency)

        if not exchange_rate:
            return Response({"error": "Exchange rate not found."}, status=status.HTTP_404_NOT_FOUND)

        converted_amount = amount * exchange_rate.rate_value
        return Response({"converted_amount": converted_amount})
    

class CurrencyCreateView(APIView):
    def post(self, request):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CurrencyDetailView(APIView):
    def get(self, request, pk):
        currency = get_currency_by_id(pk)
        if currency is None:
            return Response({"detail": "Currency not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CurrencySerializer(currency)
        return Response(serializer.data)

    def put(self, request, pk):
        currency = get_currency_by_id(pk)
        if currency is None:
            return Response({"detail": "Currency not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CurrencySerializer(currency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        currency = get_object_or_404(Currency, pk=pk)
        serializer = CurrencySerializer(currency, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        currency = get_currency_by_id(pk)
        if currency is None:
            return Response({"detail": "Currency not found."}, status=status.HTTP_404_NOT_FOUND)
        
        currency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
