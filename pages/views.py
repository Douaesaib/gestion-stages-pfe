from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import EtudiantProfileForm , SignUpForm
from .models import Etudiant,Entreprise


def home(request):
    return render(request, 'pages/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save
            auth_login(request, user) 
            if user.role == 'ETUDIANT':
                return redirect('modifier_profile')
            elif user.role == 'ENTREPRISE':
                return redirect('modifier_entreprise')
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