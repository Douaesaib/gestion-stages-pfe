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
        fields = ['cne', 'filiere', 'telephone', 'cv']
        widgets = {
            'cne': forms.TextInput(attrs={'class': 'form-control'}),
            'filiere': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            }
        

class EntrepriseProfileForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom_societe', 'secteur', 'ville', 'description', 'site_web']       