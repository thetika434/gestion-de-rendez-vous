from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from .models import Client, RendezVous


class RendezVousViewsTests(TestCase):
    def setUp(self):
        self.client_record = Client.objects.create(
            nom="Dupont",
            prenom="Alice",
            telephone="0601020304",
            email="alice@example.com",
        )
        self.other_client = Client.objects.create(
            nom="Martin",
            prenom="Bob",
            telephone="0605060708",
            email="bob@example.com",
        )
        self.rendezvous_1 = RendezVous.objects.create(
            date=date(2030, 5, 10),
            heure=time(9, 0),
            motif="Consultation",
            statut="planifie",
            client=self.client_record,
        )
        self.rendezvous_2 = RendezVous.objects.create(
            date=date(2030, 5, 11),
            heure=time(10, 0),
            motif="Suivi",
            statut="confirme",
            client=self.other_client,
        )

    def test_liste_affiche_les_rendezvous_dans_lordre_chronologique(self):
        response = self.client.get(reverse("rdv_liste"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rendezvous/rdv_liste.html")
        self.assertEqual(
            list(response.context["rendezvous_list"]),
            [self.rendezvous_1, self.rendezvous_2],
        )

    def test_liste_filtre_par_statut(self):
        response = self.client.get(reverse("rdv_liste"), {"statut": "confirme"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["rendezvous_list"]),
            [self.rendezvous_2],
        )
        self.assertEqual(response.context["statut_selectionne"], "confirme")

    def test_creation_dun_rendezvous(self):
        response = self.client.post(
            reverse("rdv_creer"),
            {
                "date": "2030-05-12",
                "heure": "11:00",
                "motif": "Première visite",
                "statut": "planifie",
                "client": self.client_record.pk,
            },
        )

        self.assertRedirects(response, reverse("rdv_liste"))
        self.assertEqual(RendezVous.objects.count(), 3)
        self.assertTrue(
            RendezVous.objects.filter(
                date=date(2030, 5, 12),
                heure=time(11, 0),
                motif="Première visite",
                statut="planifie",
                client=self.client_record,
            ).exists()
        )

    def test_modification_dun_rendezvous(self):
        response = self.client.post(
            reverse("rdv_modifier", args=[self.rendezvous_1.pk]),
            {
                "date": "2030-05-13",
                "heure": "12:30",
                "motif": "Consultation modifiée",
                "statut": "confirme",
                "client": self.other_client.pk,
            },
        )

        self.assertRedirects(response, reverse("rdv_liste"))
        self.rendezvous_1.refresh_from_db()
        self.assertEqual(self.rendezvous_1.date, date(2030, 5, 13))
        self.assertEqual(self.rendezvous_1.heure, time(12, 30))
        self.assertEqual(self.rendezvous_1.motif, "Consultation modifiée")
        self.assertEqual(self.rendezvous_1.statut, "confirme")
        self.assertEqual(self.rendezvous_1.client, self.other_client)

    def test_suppression_demande_confirmation_puis_supprime(self):
        url = reverse("rdv_supprimer", args=[self.rendezvous_1.pk])
        confirmation = self.client.get(url)

        self.assertEqual(confirmation.status_code, 200)
        self.assertTemplateUsed(confirmation, "rendezvous/rdv_confirm_delete.html")

        response = self.client.post(url)

        self.assertRedirects(response, reverse("rdv_liste"))
        self.assertFalse(
            RendezVous.objects.filter(pk=self.rendezvous_1.pk).exists()
        )
