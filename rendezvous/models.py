from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class RendezVous(models.Model):
    class Statut(models.TextChoices):
        PLANIFIE = "planifie", "Planifié"
        CONFIRME = "confirme", "Confirmé"
        TERMINE = "termine", "Terminé"
        ANNULE = "annule", "Annulé"

    date = models.DateField()
    heure = models.TimeField()
    motif = models.CharField(max_length=200)
    statut = models.CharField(
        max_length=10,
        choices=Statut.choices,
        default=Statut.PLANIFIE,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="rendez_vous",
    )

    class Meta:
        ordering = ["date", "heure"]

    def __str__(self):
        return f"{self.client} - {self.date} à {self.heure}"
