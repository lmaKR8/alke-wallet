"""URLs de la app contacts — CRUD de contactos y envío de dinero."""

from django.urls import path

from apps.contacts import views

urlpatterns = [
    path('contacts/', views.my_contacts_view, name='contact_list'),
    path('contacts/add/', views.add_contact_view, name='add_contact'),
    path('contacts/<int:pk>/edit/', views.edit_contact_view, name='edit_contact'),
    path('contacts/<int:pk>/delete/', views.delete_contact_view, name='delete_contact'),
    path('contacts/send/<int:receiver_id>/', views.send_money_view, name='send_money'),
]
