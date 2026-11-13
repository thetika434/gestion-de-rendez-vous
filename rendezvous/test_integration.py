from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from .models import Client, RendezVous


class GestionRendezVousIntegrationTests(TestCase):
    def test_creation_client_puis_rendezvous_visible_dans_la_liste(self):
        response = self.client.post(
            reverse("client_creer"),
            {
                "nom": "Kouadio",
                "prenom": "Awa",
                "telephone": "0102030405",
                "email": "awa@example.com",
            },
        )

        self.assertRedirects(response, reverse("client_liste"))
        client = Client.objects.get(email="awa@example.com")

        response = self.client.post(
            reverse("rdv_creer"),
            {
                "date": "2030-05-10",
                "heure": "09:30",
                "motif": "Consultation initiale",
                "statut": RendezVous.Statut.PLANIFIE,
                "client": client.pk,
            },
        )

        self.assertRedirects(response, reverse("rdv_liste"))
        rendezvous = RendezVous.objects.get(client=client)
        liste = self.client.get(reverse("rdv_liste"))

        self.assertEqual(rendezvous.motif, "Consultation initiale")
        self.assertContains(liste, "Awa Kouadio")
        self.assertContains(liste, "Consultation initiale")

    def test_suppression_client_supprime_aussi_ses_rendezvous(self):
        client = Client.objects.create(
            nom="Yao",
            prenom="Marc",
            email="marc@example.com",
        )
        rendezvous = RendezVous.objects.create(
            client=client,
            date=date(2030, 5, 11),
            heure=time(10, 0),
            motif="Suivi",
        )

        response = self.client.post(
            reverse("client_supprimer", args=[client.pk])
        )

        self.assertRedirects(response, reverse("client_liste"))
        self.assertFalse(Client.objects.filter(pk=client.pk).exists())
        self.assertFalse(RendezVous.objects.filter(pk=rendezvous.pk).exists())
