"""URLs de la app contacts — búsqueda de usuarios y envío de dinero."""

from django.urls import path

from apps.contacts import views

urlpatterns = [
    path('contacts/', views.contacts_view, name='contact_list'),
    path('contacts/send/<int:receiver_id>/', views.send_money_view, name='send_money'),
]
