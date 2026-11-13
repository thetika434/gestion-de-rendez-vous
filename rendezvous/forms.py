from django import forms
from django.utils import timezone

from .models import Client, RendezVous


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ["date", "heure", "motif", "statut", "client"]
        labels = {
            "date": "Date",
            "heure": "Heure",
            "motif": "Motif",
            "statut": "Statut",
            "client": "Client",
        }
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "heure": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "motif": forms.TextInput(attrs={"class": "form-control"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
            "client": forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            "date": {
                "required": "Veuillez saisir une date.",
                "invalid": "Veuillez saisir une date valide.",
            },
            "heure": {
                "required": "Veuillez saisir une heure.",
                "invalid": "Veuillez saisir une heure valide.",
            },
            "motif": {
                "required": "Veuillez saisir le motif du rendez-vous.",
                "max_length": "Le motif ne peut pas dépasser 200 caractères.",
            },
            "statut": {
                "required": "Veuillez sélectionner un statut.",
                "invalid_choice": "Veuillez sélectionner un statut valide.",
            },
            "client": {
                "required": "Veuillez sélectionner un client.",
                "invalid_choice": "Veuillez sélectionner un client valide.",
            },
        }

    def clean_date(self):
        date = self.cleaned_data["date"]
        if self.instance.pk is None and date < timezone.localdate():
            raise forms.ValidationError(
                "La date d'un nouveau rendez-vous ne peut pas être passée."
            )
        return date


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nom", "prenom", "telephone", "email"]
        labels = {
            "nom": "Nom",
            "prenom": "Prénom",
            "telephone": "Téléphone",
            "email": "Adresse e-mail",
        }
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "nom": {
                "required": "Veuillez saisir le nom du client.",
                "max_length": "Le nom ne peut pas dépasser 100 caractères.",
            },
            "prenom": {
                "required": "Veuillez saisir le prénom du client.",
                "max_length": "Le prénom ne peut pas dépasser 100 caractères.",
            },
            "telephone": {
                "max_length": "Le téléphone ne peut pas dépasser 20 caractères.",
            },
            "email": {
                "invalid": "Veuillez saisir une adresse e-mail valide.",
                "max_length": "L'adresse e-mail ne peut pas dépasser 254 caractères.",
            },
        }
