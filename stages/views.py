from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Case, When, Value, IntegerField
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone

from .models import Offre, Candidature , Entreprise


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


@login_required
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
@login_required
def offre_detail(request, offre_id):
    # كنجيبو العرض بـ ID ديالو، وإلا مالقاهش كيعطي صفحة 404
    offre = get_object_or_404(Offre, id=offre_id)
    
    return render(request, "stages/offre_detail.html", {"offre": offre})
@login_required
def mes_offres(request):
    if request.user.role != 'ENTREPRISE':
        messages.error(request, "Accès réservé aux entreprises.")
        return redirect('home')
    
    # 1. Kan-akhdou s-smia dyal ch-charika mn l'profil dyal l'utilisateur
    nom_charika = request.user.entreprise.nom_societe
    
    # 2. Kan-jbdou l'offres li smit l'entreprise dyalha (nom) kat-chbah l had s-smia
    offres = Offre.objects.filter(entreprise__nom=nom_charika).order_by('-id')
    
    return render(request, "stages/offres_list.html", {"offres": offres})

@login_required
def ajouter_offre(request):
    if request.user.role != 'ENTREPRISE':
        messages.error(request, "Accès refusé.")
        return redirect('home')

    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        competences = request.POST.get("competences")
        formation = request.POST.get("formation")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")

        # --- LA CORRECTION EST ICI ---
        # 1. On prend le nom de la société depuis le profil de l'utilisateur
        nom_charika = request.user.entreprise.nom_societe
        
        # 2. On cherche cette entreprise dans la table des stages (ou on la crée si c'est sa 1ère offre)
        entreprise_stage, created = Entreprise.objects.get_or_create(nom=nom_charika)

        # 3. On crée l'offre avec la bonne instance "entreprise_stage"
        Offre.objects.create(
            entreprise=entreprise_stage,
            titre=titre,
            description=description,
            competences=competences,
            formation=formation,
            date_debut=date_debut,
            date_fin=date_fin
        )
        # -------------------------------
        
        messages.success(request, "Votre offre de stage a été publiée avec succès ! ✅")
        return redirect('stages:mes_offres')

    return render(request, "stages/ajouter_offre.html")

@login_required
def modifier_offre(request, offre_id):
    if request.user.role != 'ENTREPRISE':
        messages.error(request, "Accès refusé.")
        return redirect('home')

    # Kan-jbdou s-smia d charika bash n-t2kdou blli had l'offre dyalha d bsse7 (Sécurité)
    nom_charika = request.user.entreprise.nom_societe
    offre = get_object_or_404(Offre, id=offre_id, entreprise__nom=nom_charika)

    if request.method == "POST":
        offre.titre = request.POST.get("titre")
        offre.description = request.POST.get("description")
        offre.competences = request.POST.get("competences")
        offre.formation = request.POST.get("formation")
        offre.date_debut = request.POST.get("date_debut")
        offre.date_fin = request.POST.get("date_fin")
        
        offre.save() # Kan-sauvegardiw l'T3dilat
        
        messages.success(request, "L'offre a été modifiée avec succès ! ✏️✅")
        return redirect('stages:mes_offres')

    return render(request, "stages/modifier_offre.html", {"offre": offre})

@login_required
def offres_list(request):
    if request.user.is_authenticated and request.user.role == 'ENTREPRISE':
        return redirect('stages:mes_offres')
        
    offres = Offre.objects.all().order_by('-id') 
    return render(request, "stages/offres_list.html", {"offres": offres})

@login_required
def mes_candidatures(request):
    candidatures = Candidature.objects.filter(email=request.user.email).order_by('-id')
    
    context = {
        'candidatures': candidatures,
        'total': candidatures.count(),
        'nb_acceptees': candidatures.filter(statut='ACCEPTEE').count(),
        'nb_en_attente': candidatures.filter(statut='EN_ATTENTE').count(),
        'nb_refusees': candidatures.filter(statut='REFUSEE').count(),
    }
    
    return render(request, 'stages/mes_candidatures.html', context)


from django.http import FileResponse, Http404

@login_required
def telecharger_convention(request, candidature_id):
    """Génère et retourne la convention de stage (via ReportLab)."""
    from analytics.utils_pdf import generer_pdf_convention
    candidature = get_object_or_404(Candidature, id=candidature_id)

    # Sécurité : seul le propriétaire peut télécharger sa convention
    if candidature.email != request.user.email:
        raise Http404("Convention introuvable.")

    # Seules les candidatures acceptées ont une convention
    if candidature.statut != 'ACCEPTEE':
        messages.error(request, "La convention n'est disponible que pour les candidatures acceptées.")
        return redirect('stages:mes_candidatures')

    # Génération du PDF avec les vraies données
    nom_stagiaire = f"{candidature.nom_stagiaire} {candidature.prenom_stagiaire or ''}".strip()
    entreprise = candidature.offre.entreprise
    nom_entreprise = entreprise.nom
    adresse_entreprise = entreprise.adresse or "Adresse non renseignée"
    
    # On met "Le Directeur" par défaut pour le responsable
    responsable_entreprise = "Le Directeur / Ressources Humaines"
    
    # Récupération de la filière de l'étudiant s'il a un profil
    try:
        filiere_stagiaire = request.user.etudiant.filiere or "Génie Informatique"
    except Exception:
        filiere_stagiaire = "Ingénierie & Développement"
        
    # Année universitaire calculée automatiquement
    import datetime
    annee = datetime.datetime.now().year
    # Si on est avant septembre, c'est l'année en cours - 1 / l'année en cours
    if datetime.datetime.now().month < 9:
        annee_universitaire = f"{annee-1}/{annee}"
    else:
        annee_universitaire = f"{annee}/{annee+1}"

    buffer = generer_pdf_convention(
        stagiaire_nom=nom_stagiaire, 
        entreprise_nom=nom_entreprise,
        entreprise_adresse=adresse_entreprise,
        entreprise_responsable=responsable_entreprise,
        stagiaire_filiere=filiere_stagiaire,
        annee_universitaire=annee_universitaire
    )
    
    filename = f"convention_stage_{candidature.nom_stagiaire}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)
