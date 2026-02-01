from django.shortcuts import render
from .utils_pdf import generer_pdf_convention
from django.http import FileResponse, HttpResponse
from .ai_matching import calculer_score_matching
from stages.models import Offre, Entreprise
from django.contrib.auth.decorators import login_required
from stages.models import Offre
from users.models import Stagiaire


def dashboard_view(request):
    #en remplace plus tard par Stagiaire.objects.count()
    context = {
        'nb_stagiaires': Stagiaire.objects.count(),
        'nb_entreprise': Entreprise.objects.count(),
        'nb_offres': Offre.objects.count(),
        'nb_convention': 98,
    }
    return render(request, 'analytics/dashboard.html', context)


def download_convention(request):
    buffer = generer_pdf_convention()
    return FileResponse(buffer, as_attachment=True, filename='convention_stage.pdf')

def test_ai_matching(request):
    # Simulation des données (Mocking)
    
    # Scénario : Un étudiant doué en Python postule à une offre Java
    cv_etudiant = "java , python , c "
    offre_stage = "c++, python , java"
    
    # Appel de l'IA
    score = calculer_score_matching(cv_etudiant, offre_stage)
    
    return HttpResponse(f"<h1>Test IA Matching</h1><p>CV : {cv_etudiant}</p><p>Offre : {offre_stage}</p><h2>Score de compatibilité : {score}%</h2>")

def demo_ai_view(request):
    score = None
    cv_text = ""
    offre_text = ""
    color = "red" # Couleur par défaut

    if request.method == 'POST':
        # On récupère le texte tapé par l'utilisateur
        cv_text = request.POST.get('cv_text', '')
        offre_text = request.POST.get('offre_text', '')
        
        # On lance l'IA
        if cv_text and offre_text:
            score = calculer_score_matching(cv_text, offre_text)
            
            # Petite logique pour la couleur
            if score < 30:
                color = "#dc3545" # Rouge
            elif score < 60:
                color = "#ffc107" # Orange
            else:
                color = "#28a745" # Vert

    context = {
        'score': score,
        'cv_text': cv_text,
        'offre_text': offre_text,
        'color': color
    }
    return render(request, 'analytics/demo_ai.html', context)


@login_required
def recommandations_view(request):
    # 1. Recuperer l'étudiant
    try:
        le_stagiaire = Stagiaire.objects.get(user=request.user)
        mes_competences = le_stagiaire.competences
        nom_complet = f"{request.user.first_name} {request.user.last_name}"
    except Stagiaire.DoesNotExist:
        # Cas Secours
        mes_competences = "Python, Django, SQL" 
        nom_complet = "Administrateur"

    offres_db = Offre.objects.all()
    offres_recommandees = []

    # 3. Traitement IA
    for offre in offres_db:
        texte_offre = f"{offre.titre} {offre.description}" 
        
        score = calculer_score_matching(mes_competences, texte_offre)
        offre.score_calcule = score
        
        if score > 20:
            offres_recommandees.append(offre)

    # 4. Tri par score
    offres_recommandees.sort(key=lambda x: x.score_calcule, reverse=True)

    return render(request, 'analytics/recommandations.html', {
        'etudiant': {"nom": nom_complet, "competences": mes_competences},
        'recommandations': offres_recommandees
    })