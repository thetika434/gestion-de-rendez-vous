from django.urls import path

from . import views_rendezvous


urlpatterns = [
    path("", views_rendezvous.rdv_liste, name="rdv_liste"),
    path("creer/", views_rendezvous.rdv_creer, name="rdv_creer"),
    path("<int:pk>/modifier/", views_rendezvous.rdv_modifier, name="rdv_modifier"),
    path("<int:pk>/supprimer/", views_rendezvous.rdv_supprimer, name="rdv_supprimer"),
]
