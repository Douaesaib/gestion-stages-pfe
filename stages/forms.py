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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            from .validators import is_valid_email
            if not is_valid_email(email):
                raise forms.ValidationError("Veuillez saisir une adresse email valide.")
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            from .validators import is_valid_phone
            if not is_valid_phone(telephone):
                raise forms.ValidationError("Numéro de téléphone invalide (ex: 06XXXXXXXX ou +2126XXXXXXXX).")
        return telephone
