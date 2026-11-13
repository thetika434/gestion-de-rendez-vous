from django.urls import path

from . import views_clients


urlpatterns = [
    path("", views_clients.client_liste, name="client_liste"),
    path("creer/", views_clients.client_creer, name="client_creer"),
    path("<int:pk>/modifier/", views_clients.client_modifier, name="client_modifier"),
    path("<int:pk>/supprimer/", views_clients.client_supprimer, name="client_supprimer"),
]
