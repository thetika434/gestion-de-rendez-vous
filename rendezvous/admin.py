from django.contrib import admin

from .models import Client, RendezVous


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "telephone", "email")
    search_fields = ("nom", "prenom")


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ("date", "heure", "motif", "statut", "client")
    list_filter = ("statut",)
    search_fields = ("client__nom", "client__prenom")
