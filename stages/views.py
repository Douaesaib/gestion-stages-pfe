from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Case, When, Value, IntegerField

from .models import Offre, Candidature


def offres_list(request):
    offres = (
        Offre.objects
        .select_related("entreprise")
        .annotate(
            priority=Case(
                # 0) DEV / Software / Web
                When(
                    Q(titre__icontains="dev") |
                    Q(description__icontains="dev") |
                    Q(entreprise__secteur__icontains="dev") |
                    Q(titre__icontains="dévelop") |
                    Q(description__icontains="dévelop") |
                    Q(titre__icontains="develop") |
                    Q(description__icontains="develop") |
                    Q(titre__icontains="developer") |
                    Q(description__icontains="developer") |
                    Q(titre__icontains="software") |
                    Q(description__icontains="software") |
                    Q(titre__icontains="programm") |
                    Q(description__icontains="programm") |
                    Q(titre__icontains="web") |
                    Q(description__icontains="web") |
                    Q(titre__icontains="frontend") |
                    Q(description__icontains="frontend") |
                    Q(titre__icontains="backend") |
                    Q(description__icontains="backend") |
                    Q(titre__icontains="full stack") |
                    Q(description__icontains="full stack") |
                    Q(titre__icontains="fullstack") |
                    Q(description__icontains="fullstack") |
                    Q(titre__icontains="django") |
                    Q(description__icontains="django") |
                    Q(titre__icontains="react") |
                    Q(description__icontains="react") |
                    Q(titre__icontains="node") |
                    Q(description__icontains="node"),
                    then=Value(0)
                ),

                # 1) DATA / IT / INFORMATIQUE
                When(
                    Q(titre__icontains="data") |
                    Q(description__icontains="data") |
                    Q(entreprise__secteur__icontains="data") |
                    Q(titre__icontains="sql") |
                    Q(description__icontains="sql") |
                    Q(titre__icontains="bi") |
                    Q(description__icontains="bi") |
                    Q(titre__icontains="analytics") |
                    Q(description__icontains="analytics") |
                    Q(titre__icontains="informatique") |
                    Q(description__icontains="informatique") |
                    Q(entreprise__secteur__icontains="informatique") |
                    Q(titre__icontains="it") |
                    Q(description__icontains="it") |
                    Q(entreprise__secteur__icontains="it") |
                    Q(titre__icontains="info") |
                    Q(description__icontains="info") |
                    Q(entreprise__secteur__icontains="info") |
                    Q(titre__icontains="cloud") |
                    Q(description__icontains="cloud") |
                    Q(titre__icontains="api") |
                    Q(description__icontains="api"),
                    then=Value(1)
                ),

                # 2) CYBER / SÉCURITÉ / RÉSEAUX
                When(
                    Q(titre__icontains="cyber") |
                    Q(description__icontains="cyber") |
                    Q(entreprise__secteur__icontains="cyber") |
                    Q(titre__icontains="sécurité") |
                    Q(description__icontains="sécurité") |
                    Q(titre__icontains="security") |
                    Q(description__icontains="security") |
                    Q(titre__icontains="réseau") |
                    Q(description__icontains="réseau") |
                    Q(titre__icontains="reseau") |
                    Q(description__icontains="reseau") |
                    Q(titre__icontains="network") |
                    Q(description__icontains="network") |
                    Q(entreprise__secteur__icontains="réseau") |
                    Q(entreprise__secteur__icontains="reseau") |
                    Q(entreprise__secteur__icontains="network"),
                    then=Value(2)
                ),

                default=Value(3),
                output_field=IntegerField()
            )
        )
        .order_by("priority", "-id") 
    )

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
