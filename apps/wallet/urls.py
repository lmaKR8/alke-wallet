"""URLs de la app wallet — landing, dashboard y depósitos."""

from django.urls import path

from apps.wallet import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
]
