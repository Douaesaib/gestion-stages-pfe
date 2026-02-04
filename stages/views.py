from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Offre, Candidature


def offres_list(request):
    offres = Offre.objects.select_related("entreprise").all().order_by("-id")
    return render(request, "stages/offres_list.html", {"offres": offres})


def postuler(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == "POST":
        nom = (request.POST.get("nom_stagiaire") or "").strip()
        prenom = (request.POST.get("prenom_stagiaire") or "").strip()
        email = (request.POST.get("email") or "").strip()
        telephone = (request.POST.get("telephone") or "").strip()
        cv = request.FILES.get("cv")  # ملف ال CV

        if not nom:
            messages.error(request, "Veuillez saisir votre nom.")
            return render(request, "stages/postuler.html", {"offre": offre})

        if not prenom:
            messages.error(request, "Veuillez saisir votre prénom.")
            return render(request, "stages/postuler.html", {"offre": offre})

        if not email:
            messages.error(request, "Veuillez saisir votre email.")
            return render(request, "stages/postuler.html", {"offre": offre})

        if not telephone:
            messages.error(request, "Veuillez saisir votre téléphone.")
            return render(request, "stages/postuler.html", {"offre": offre})

        if not cv:
            messages.error(request, "Veuillez uploader votre CV (PDF).")
            return render(request, "stages/postuler.html", {"offre": offre})

        existe_deja = Candidature.objects.filter(
            offre=offre,
            nom_stagiaire=nom,
            prenom_stagiaire=prenom
        ).exists()

        if existe_deja:
            messages.warning(request, "Vous avez déjà postulé à cette offre.")
            return redirect("stages:offres_list")

        Candidature.objects.create(
            offre=offre,
            nom_stagiaire=nom,
            prenom_stagiaire=prenom,
            email=email,
            telephone=telephone,
            cv=cv
        )

        messages.success(request, "Votre candidature a été envoyée ✅")
        return redirect("stages:offres_list")

    return render(request, "stages/postuler.html", {"offre": offre})
