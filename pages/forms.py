from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Etudiant, Entreprise, Encadrant

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            from stages.validators import is_valid_email
            if not is_valid_email(email):
                raise forms.ValidationError("Veuillez saisir une adresse email valide.")
        return email

class EtudiantProfileForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['cne', 'filiere', 'telephone', 'ecole', 'niveau_etudes', 'competences', 'experiences', 'projets', 'cv_file']
        widgets = {
            'cne': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'ecole': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ecole / Université'}),
            'filiere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Filière'}),
            'competences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Python, Java, SQL...'}),
            'projets': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de vos projets'}),
            'experiences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Stages ou expériences passées'}),
            'cv_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
            
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            from stages.validators import is_valid_phone
            if not is_valid_phone(telephone):
                raise forms.ValidationError("Numéro de téléphone invalide (ex: 06XXXXXXXX ou +2126XXXXXXXX).")
        return telephone
            
        

class EntrepriseProfileForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom_societe', 'secteur', 'ville', 'description', 'site_web']       

class EncadrantProfileForm(forms.ModelForm):
    class Meta:
        model = Encadrant
        fields = ['departement', 'specialite', 'telephone']
        widgets = {
            'departement': forms.TextInput(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            from stages.validators import is_valid_phone
            if not is_valid_phone(telephone):
                raise forms.ValidationError("Numéro de téléphone invalide (ex: 06XXXXXXXX ou +2126XXXXXXXX).")
        return telephone