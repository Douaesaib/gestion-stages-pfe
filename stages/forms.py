from django import forms
from .models import Candidature


class PostulerForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ["nom_stagiaire", "prenom_stagiaire", "email", "telephone", "cv"]
        widgets = {
            "nom_stagiaire": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom"}),
            "prenom_stagiaire": forms.TextInput(attrs={"class": "form-control", "placeholder": "Prénom"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "telephone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Téléphone"}),
            "cv": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
