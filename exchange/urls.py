from django.urls import path
from .views import CurrencyListView, CurrencyExchangeRateListView, CurrencyExchangeRateConvertView
from exchange import views

urlpatterns = [
    path('currencies/', views.CurrencyListView.as_view(), name='currency-list'),    
    path('currencies/create/', views.CurrencyCreateView.as_view(), name='currency-create'),
    path('currencies/<int:pk>/', views.CurrencyDetailView.as_view(), name='currency-detail'),
    path('exchange-rates/', views.CurrencyExchangeRateListView.as_view(), name='exchange-rate-list'),
    path('convert/', views.CurrencyExchangeRateConvertView.as_view(), name='exchange-rate-convert'),
]
