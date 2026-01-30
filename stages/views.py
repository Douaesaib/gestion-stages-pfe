from django.shortcuts import render, get_object_or_404, redirect
from .models import Offre, Candidature


def offres_list(request):
    offres = Offre.objects.select_related("entreprise").all().order_by("-id")
    return render(request, "stages/offres_list.html", {"offres": offres})


def postuler(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == "POST":
        nom = request.POST.get("nom_stagiaire", "").strip()
        if nom:
            Candidature.objects.create(offre=offre, nom_stagiaire=nom)
            return redirect("stages:offres_list")

    return render(request, "stages/postuler.html", {"offre": offre})

