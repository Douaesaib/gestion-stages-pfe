from django.contrib import admin
from .models import Entreprise, Offre, Candidature


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("nom", "secteur", "email", "telephone")
    search_fields = ("nom", "secteur", "email")


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ("titre", "entreprise", "date_debut", "date_fin")
    list_filter = ("entreprise",)
    search_fields = ("titre", "entreprise__nom")


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ("nom_stagiaire", "offre", "date_candidature")
    list_filter = ("offre",)
    search_fields = ("nom_stagiaire",)
