from django.shortcuts import get_object_or_404, redirect, render

from .forms import RendezVousForm
from .models import RendezVous


def rdv_liste(request):
    rendezvous = RendezVous.objects.select_related("client").order_by("date", "heure")
    statut = request.GET.get("statut", "")
    if statut:
        rendezvous = rendezvous.filter(statut=statut)

    return render(
        request,
        "rendezvous/rdv_liste.html",
        {"rendezvous_list": rendezvous, "statut_selectionne": statut},
    )


def rdv_creer(request):
    form = RendezVousForm(
        request.POST if request.method == "POST" else None
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("rdv_liste")

    return render(request, "rendezvous/rdv_form.html", {"form": form})


def rdv_modifier(request, pk):
    rendezvous = get_object_or_404(RendezVous, pk=pk)
    form = RendezVousForm(
        request.POST if request.method == "POST" else None,
        instance=rendezvous,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("rdv_liste")

    return render(
        request,
        "rendezvous/rdv_form.html",
        {"form": form, "rendezvous": rendezvous},
    )


def rdv_supprimer(request, pk):
    rendezvous = get_object_or_404(RendezVous, pk=pk)
    if request.method == "POST":
        rendezvous.delete()
        return redirect("rdv_liste")

    return render(
        request,
        "rendezvous/rdv_confirm_delete.html",
        {"rendezvous": rendezvous},
    )
