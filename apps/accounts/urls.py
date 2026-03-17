"""URLs de la app accounts — login, registro y logout."""

from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
