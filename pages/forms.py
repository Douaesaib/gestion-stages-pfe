from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Etudiant,Entreprise

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'email',)

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
            
        

class EntrepriseProfileForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom_societe', 'secteur', 'ville', 'description', 'site_web']       