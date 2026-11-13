from django.test import TestCase
from django.urls import reverse

from .models import Client


class ClientViewsTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            nom="Kouassi",
            prenom="Awa",
            telephone="0102030405",
            email="awa@example.com",
        )

    def test_liste_affiche_les_clients(self):
        response = self.client.get(reverse("client_liste"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Awa Kouassi")
        self.assertTemplateUsed(response, "clients/client_liste.html")

    def test_creation_d_un_client(self):
        response = self.client.post(
            reverse("client_creer"),
            {
                "nom": "Yao",
                "prenom": "Marc",
                "telephone": "0708091011",
                "email": "marc@example.com",
            },
        )

        self.assertRedirects(response, reverse("client_liste"))
        self.assertTrue(Client.objects.filter(nom="Yao", prenom="Marc").exists())

    def test_modification_d_un_client(self):
        response = self.client.post(
            reverse("client_modifier", args=[self.client_obj.pk]),
            {
                "nom": "Kone",
                "prenom": "Awa",
                "telephone": "0102030405",
                "email": "awa.kone@example.com",
            },
        )

        self.assertRedirects(response, reverse("client_liste"))
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.nom, "Kone")
        self.assertEqual(self.client_obj.email, "awa.kone@example.com")

    def test_suppression_affiche_confirmation_puis_supprime(self):
        url = reverse("client_supprimer", args=[self.client_obj.pk])
        response_confirmation = self.client.get(url)

        self.assertEqual(response_confirmation.status_code, 200)
        self.assertContains(response_confirmation, "Confirmez-vous la suppression")
        self.assertTrue(Client.objects.filter(pk=self.client_obj.pk).exists())

        response_suppression = self.client.post(url)

        self.assertRedirects(response_suppression, reverse("client_liste"))
        self.assertFalse(Client.objects.filter(pk=self.client_obj.pk).exists())
