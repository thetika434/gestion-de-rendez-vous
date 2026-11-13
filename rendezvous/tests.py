from datetime import date, time, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Client, RendezVous


class ClientModelTests(TestCase):
    def test_create_client_with_optional_fields_blank(self):
        client = Client.objects.create(
            nom="Diallo",
            prenom="Aminata",
            telephone="",
            email="",
        )

        self.assertEqual(str(client), "Aminata Diallo")


class RendezVousModelTests(TestCase):
    def setUp(self):
        self.client = Client.objects.create(nom="Diallo", prenom="Aminata")
        self.date = date(2026, 6, 1)
        self.heure = time(9, 0)

    def create_rendez_vous(self, **overrides):
        values = {
            "client": self.client,
            "date": self.date,
            "heure": self.heure,
            "motif": "Consultation",
        }
        values.update(overrides)
        return RendezVous.objects.create(**values)

    def test_create_rendez_vous_defaults_to_planifie_and_has_string(self):
        rendez_vous = self.create_rendez_vous()

        self.assertEqual(rendez_vous.statut, RendezVous.Statut.PLANIFIE)
        self.assertEqual(
            str(rendez_vous),
            "Aminata Diallo - 2026-06-01 à 09:00:00",
        )

    def test_rendez_vous_are_ordered_by_date_then_time(self):
        later = self.create_rendez_vous(heure=time(11, 0))
        next_day = self.create_rendez_vous(date=self.date + timedelta(days=1))
        earlier = self.create_rendez_vous(heure=time(8, 0))

        self.assertEqual(
            list(RendezVous.objects.all()),
            [earlier, later, next_day],
        )

    def test_clean_rejects_another_active_appointment_at_same_time(self):
        self.create_rendez_vous()
        duplicate = RendezVous(
            client=self.client,
            date=self.date,
            heure=self.heure,
            motif="Suivi",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_cancelled_appointment_can_overlap_an_active_appointment(self):
        self.create_rendez_vous()
        cancelled = RendezVous(
            client=self.client,
            date=self.date,
            heure=self.heure,
            motif="Annulé",
            statut=RendezVous.Statut.ANNULE,
        )

        cancelled.full_clean()

    def test_active_appointment_can_use_slot_of_cancelled_appointment(self):
        self.create_rendez_vous(statut=RendezVous.Statut.ANNULE)
        replacement = RendezVous(
            client=self.client,
            date=self.date,
            heure=self.heure,
            motif="Nouveau rendez-vous",
        )

        replacement.full_clean()
