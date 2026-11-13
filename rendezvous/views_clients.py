from django import forms
from django.shortcuts import get_object_or_404, redirect, render

from .models import Client

try:
    from .forms import ClientForm
except ImportError:
    # Le formulaire partagé par Koffi n'est pas encore présent sur main.
    class ClientForm(forms.ModelForm):
        class Meta:
            model = Client
            fields = ["nom", "prenom", "telephone", "email"]


def client_liste(request):
    clients = Client.objects.all().order_by("nom", "prenom", "pk")
    return render(request, "clients/client_liste.html", {"clients": clients})


def client_creer(request):
    form = ClientForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("client_liste")

    return render(request, "clients/client_form.html", {"form": form})


def client_modifier(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("client_liste")

    return render(
        request,
        "clients/client_form.html",
        {"form": form, "client": client},
    )


def client_supprimer(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()
        return redirect("client_liste")

    return render(
        request,
        "clients/client_confirm_delete.html",
        {"client": client},
    )
