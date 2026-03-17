"""URLs de la app transactions — historial de transacciones."""

from django.urls import path

from apps.transactions import views

urlpatterns = [
    path('transactions/', views.transaction_list_view, name='transaction_list'),
]
