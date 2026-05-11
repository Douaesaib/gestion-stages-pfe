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


@login_required
def telecharger_convention(request, candidature_id):
    """Génère et retourne la convention de stage au format HTML imprimable (PDF via navigateur)."""
    candidature = get_object_or_404(Candidature, id=candidature_id)

    # Sécurité : seul le propriétaire peut télécharger sa convention
    if candidature.email != request.user.email:
        raise Http404("Convention introuvable.")

    # Seules les candidatures acceptées ont une convention
    if candidature.statut != 'ACCEPTEE':
        messages.error(request, "La convention n'est disponible que pour les candidatures acceptées.")
        return redirect('stages:mes_candidatures')

    today = timezone.now().date()
    offre = candidature.offre
    entreprise = offre.entreprise

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Convention de Stage — {candidature.nom_stagiaire} {candidature.prenom_stagiaire or ''}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', Arial, sans-serif; font-size: 13px; color: #1a1a2e; background: #fff; padding: 40px; }}
  .header {{ text-align: center; border-bottom: 3px solid #3b28cc; padding-bottom: 20px; margin-bottom: 30px; }}
  .header h1 {{ font-size: 22px; color: #3b28cc; font-weight: 700; letter-spacing: -0.5px; }}
  .header p {{ color: #666; font-size: 12px; margin-top: 4px; }}
  .logo-text {{ font-size: 28px; font-weight: 800; color: #3b28cc; letter-spacing: -1px; }}
  .logo-text span {{ color: #00c8ff; }}
  .section {{ margin-bottom: 24px; }}
  .section-title {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; color: #3b28cc; font-weight: 700; border-left: 3px solid #3b28cc; padding-left: 10px; margin-bottom: 12px; }}
  .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .info-item {{ background: #f8f9ff; border-radius: 8px; padding: 10px 14px; border: 1px solid #e8e9ff; }}
  .info-item label {{ display: block; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 3px; }}
  .info-item value {{ font-weight: 600; color: #1a1a2e; font-size: 13px; }}
  .clause {{ background: #f8f9ff; border-radius: 8px; padding: 14px; margin-bottom: 10px; border-left: 3px solid #e0e0ff; }}
  .clause h4 {{ font-size: 12px; font-weight: 700; color: #3b28cc; margin-bottom: 6px; }}
  .clause p {{ color: #444; line-height: 1.6; font-size: 12px; }}
  .signatures {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 40px; }}
  .sig-box {{ text-align: center; border-top: 1px solid #ccc; padding-top: 10px; }}
  .sig-box p {{ font-size: 11px; color: #666; }}
  .sig-box strong {{ display: block; font-size: 12px; color: #1a1a2e; margin-top: 4px; }}
  .footer {{ text-align: center; margin-top: 40px; font-size: 10px; color: #aaa; border-top: 1px solid #eee; padding-top: 12px; }}
  @media print {{
    body {{ padding: 20px; }}
    @page {{ margin: 15mm; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div class="logo-text">TalentSync <span>AI</span></div>
  <h1>CONVENTION DE STAGE DE FIN D'ÉTUDES (PFE)</h1>
  <p>Établie le {today.strftime('%d/%m/%Y')} — N° {candidature.id:05d}</p>
</div>

<div class="section">
  <div class="section-title">Stagiaire</div>
  <div class="info-grid">
    <div class="info-item"><label>Nom complet</label><value>{candidature.nom_stagiaire} {candidature.prenom_stagiaire or ''}</value></div>
    <div class="info-item"><label>Email</label><value>{candidature.email or '—'}</value></div>
    <div class="info-item"><label>Téléphone</label><value>{candidature.telephone or '—'}</value></div>
    <div class="info-item"><label>Date de candidature</label><value>{candidature.date_candidature.strftime('%d/%m/%Y') if candidature.date_candidature else '—'}</value></div>
  </div>
</div>

<div class="section">
  <div class="section-title">Entreprise d'accueil</div>
  <div class="info-grid">
    <div class="info-item"><label>Nom</label><value>{entreprise.nom}</value></div>
    <div class="info-item"><label>Secteur</label><value>{entreprise.secteur or '—'}</value></div>
    <div class="info-item"><label>Adresse</label><value>{entreprise.adresse or '—'}</value></div>
    <div class="info-item"><label>Email</label><value>{entreprise.email or '—'}</value></div>
  </div>
</div>

<div class="section">
  <div class="section-title">Stage</div>
  <div class="info-grid">
    <div class="info-item"><label>Intitulé du poste</label><value>{offre.titre}</value></div>
    <div class="info-item"><label>Durée</label><value>{offre.date_debut} → {offre.date_fin}</value></div>
  </div>
  {'<div class="info-item" style="margin-top:10px;grid-column:span 2;"><label>Description</label><value>' + offre.description[:300] + '...</value></div>' if offre.description else ''}
</div>

<div class="section">
  <div class="section-title">Clauses de la convention</div>
  <div class="clause">
    <h4>Article 1 — Objet</h4>
    <p>La présente convention a pour objet de définir les modalités du stage de fin d'études effectué par l'étudiant(e) au sein de l'entreprise d'accueil, dans le cadre de l'obtention de son diplôme.</p>
  </div>
  <div class="clause">
    <h4>Article 2 — Durée</h4>
    <p>Le stage se déroulera du <strong>{offre.date_debut}</strong> au <strong>{offre.date_fin}</strong>. La durée totale est conforme aux exigences académiques.</p>
  </div>
  <div class="clause">
    <h4>Article 3 — Obligations de l'entreprise</h4>
    <p>L'entreprise s'engage à accueillir le stagiaire dans de bonnes conditions, à lui fournir un encadrement adéquat, et à préserver la confidentialité de son travail académique.</p>
  </div>
  <div class="clause">
    <h4>Article 4 — Obligations du stagiaire</h4>
    <p>Le stagiaire s'engage à respecter le règlement intérieur de l'entreprise, à rédiger un rapport de stage, et à respecter la confidentialité des informations auxquelles il aura accès.</p>
  </div>
</div>

<div class="signatures">
  <div class="sig-box">
    <p>Le stagiaire</p>
    <br><br>
    <strong>{candidature.nom_stagiaire} {candidature.prenom_stagiaire or ''}</strong>
  </div>
  <div class="sig-box">
    <p>L'établissement</p>
    <br><br>
    <strong>Faculté des Sciences — Tétouan</strong>
  </div>
  <div class="sig-box">
    <p>L'entreprise d'accueil</p>
    <br><br>
    <strong>{entreprise.nom}</strong>
  </div>
</div>

<div class="footer">
  <p>Convention générée automatiquement par TalentSync AI · Plateforme de Gestion des Stages PFE<br>
  Ce document est valide uniquement avec les signatures des trois parties.</p>
</div>

<script>window.onload = function() {{ window.print(); }}</script>
</body>
</html>"""

    response = HttpResponse(html, content_type='text/html; charset=utf-8')
    filename = f"convention_stage_{candidature.nom_stagiaire}_{candidature.id}.html"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response