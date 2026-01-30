from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Offre, Candidature


def offres_list(request):
    offres = Offre.objects.select_related("entreprise").all().order_by("-id")
    return render(request, "stages/offres_list.html", {"offres": offres})


def postuler(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == "POST":
        nom = request.POST.get("nom_stagiaire", "").strip()

        if not nom:
            messages.error(request, "Veuillez saisir votre nom.")
            return render(request, "stages/postuler.html", {"offre": offre})

        # منع نفس الاسم يترشح لنفس العرض مرة أخرى
        existe_deja = Candidature.objects.filter(offre=offre, nom_stagiaire=nom).exists()
        if existe_deja:
            messages.warning(request, "Vous avez déjà postulé à cette offre.")
            return redirect("stages:offres_list")

        Candidature.objects.create(offre=offre, nom_stagiaire=nom)
        messages.success(request, "Votre candidature a été envoyée ✅")
        return redirect("stages:offres_list")

    return render(request, "stages/postuler.html", {"offre": offre})
