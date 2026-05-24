# 🌟 ZEDNA get_object_or_404 HNA
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import EtudiantProfileForm, EntrepriseProfileForm, SignUpForm, EncadrantProfileForm
from .models import Etudiant, Entreprise, Encadrant
from django.contrib import messages
from stages.models import Candidature, Offre


def home(request):
    return render(request, 'pages/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            if user.role == 'ETUDIANT':
                return redirect('modifier_profile')
            elif user.role == 'ENTREPRISE':
                return redirect('modifier_entreprise')
            elif user.role == 'ENCADRANT':
                return redirect('modifier_encadrant')
            else:
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})

@login_required
def modifier_profile(request):
    if request.user.role != 'ETUDIANT':
        return redirect('home')

    etudiant, created = Etudiant.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EtudiantProfileForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EtudiantProfileForm(instance=etudiant)
        
    return render(request, 'pages/modifier_profile.html', {'form': form})

@login_required
def modifier_entreprise(request):
    if request.user.role != 'ENTREPRISE':
        return redirect('home')

    entreprise, created = Entreprise.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EntrepriseProfileForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EntrepriseProfileForm(instance=entreprise)
        
    return render(request, 'pages/modifier_entreprise.html', {'form': form})

@login_required
def modifier_encadrant(request):
    if request.user.role != 'ENCADRANT':
        return redirect('home')

    encadrant, created = Encadrant.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EncadrantProfileForm(request.POST, request.FILES, instance=encadrant)
        if form.is_valid():
            form.save()
            return redirect('stages:dashboard_encadrant')
    else:
        form = EncadrantProfileForm(instance=encadrant)
        
    return render(request, 'pages/modifier_encadrant.html', {'form': form})

@login_required
def remplir_cv(request):
    try:
        etudiant = request.user.etudiant
    except Etudiant.DoesNotExist:
        etudiant = None

    if request.method == 'POST':
        form = EtudiantProfileForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            raw_skills = form.cleaned_data['competences']
            skills_list = [s.strip().lower() for s in raw_skills.split(',')]
            
            return redirect('home') # 🌟 Bddlna success_url li kant khawya
    else:
        form = EtudiantProfileForm(instance=etudiant)
        
    return render(request, 'cv.html', {'form': form})

# ====================================================================
# 🌟 FONCTIONS GESTION DES CANDIDATURES (CORRIGÉES & PROPRES)
# ====================================================================
@login_required
def candidatures_recues(request):
    if request.user.role != 'ENTREPRISE':
        return redirect('home')

    # Bima anna request.user.entreprise fiha smit sh-charika ("NTT DATA")
    nom_societe = request.user.entreprise 
    
    # 🌟 KAN-ZIDOU __nom HNA BASH DJANGO Y-QRAH STR NISHAN
    candidatures = Candidature.objects.filter(offre__entreprise__nom=nom_societe).order_by('-id')
        
    return render(request, 'stages/candidatures_recues.html', {'candidatures': candidatures})

@login_required
def changer_statut_candidature(request, candidature_id, nouveau_statut):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    
    if nouveau_statut in ['ACCEPTEE', 'REFUSEE']:
        candidature.statut = nouveau_statut
        candidature.save()
        
        if nouveau_statut == 'ACCEPTEE':
            # Récupérer les infos du tuteur depuis le POST (si présentes)
            tuteur_nom = request.POST.get('tuteur_nom')
            tuteur_email = (request.POST.get('tuteur_email') or '').strip()
            tuteur_poste = request.POST.get('tuteur_poste')

            if tuteur_email:
                from stages.validators import is_valid_email
                if not is_valid_email(tuteur_email):
                    messages.error(request, "Veuillez saisir une adresse email valide pour le tuteur.")
                    return redirect('candidatures_recues')
            
            from stages.views import auto_creer_stage_actif
            auto_creer_stage_actif(candidature, tuteur_nom, tuteur_email, tuteur_poste)
            messages.success(request, f"Félicitations ! Candidature acceptée et tuteur affecté ✅")
        else:
            messages.success(request, f"Le statut a été mis à jour : {nouveau_statut}")
    
    return redirect('candidatures_recues')
@login_required
def soumettre_bilan_entreprise(request, stage_id):
    if request.user.role != 'ENTREPRISE':
        return redirect('home')

    from stages.models import StageActif
    stage = get_object_or_404(StageActif, id=stage_id)
    
    if request.method == 'POST':
        stage.note_assiduite = request.POST.get('note_assiduite', 0)
        stage.note_technique = request.POST.get('note_technique', 0)
        stage.note_integration = request.POST.get('note_integration', 0)
        stage.feedback_entreprise = request.POST.get('feedback_entreprise', '').strip()
        stage.save()
        messages.success(request, "Bilan de fin de stage enregistré avec succès ! ⭐")
        
    return redirect('candidatures_recues')
