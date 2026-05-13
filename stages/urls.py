from django.urls import path
from . import views

app_name = "stages"

urlpatterns = [
    path("offres/", views.offres_list, name="offres_list"),
    path("offres/<int:offre_id>/", views.offre_detail, name="detail_offre"),
    path("offres/<int:offre_id>/postuler/", views.postuler, name="postuler"),
    path("mes-offres/", views.mes_offres, name="mes_offres"),
    path("mes-offres/ajouter/", views.ajouter_offre, name="ajouter_offre"),
    path("mes-offres/modifier/<int:offre_id>/", views.modifier_offre, name="modifier_offre"),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('telecharger-convention/<int:candidature_id>/', views.telecharger_convention, name='telecharger_convention'),
    # Encadrant
    path('encadrant/dashboard/', views.dashboard_encadrant, name='dashboard_encadrant'),
    path('encadrant/prendre-en-charge/<int:stage_id>/', views.prendre_en_charge, name='prendre_en_charge'),
    path('encadrant/evaluation/<int:stage_id>/', views.soumettre_evaluation, name='soumettre_evaluation'),
    path('encadrant/telecharger-rapport/<int:stage_id>/', views.telecharger_rapport, name='telecharger_rapport'),
    # Etudiant - dépôt rapport (legacy)
    path('deposer-rapport/', views.deposer_rapport, name='deposer_rapport'),
    # Etudiant - livrables
    path('deposer-livrable/', views.deposer_livrable, name='deposer_livrable'),
    # Entreprise - feedback
    path('feedback-entreprise/<int:stage_id>/', views.soumettre_feedback_entreprise, name='feedback_entreprise'),
    # Encadrant - télécharger livrable (marque comme téléchargé)
    path('encadrant/livrable/<int:livrable_id>/', views.telecharger_livrable, name='telecharger_livrable'),
    # Encadrant - valider sujet (toggle)
    path('encadrant/valider-sujet/<int:stage_id>/', views.valider_sujet, name='valider_sujet'),
    # Encadrant - renseigner tuteur entreprise
    path('encadrant/tuteur/<int:stage_id>/', views.maj_tuteur_entreprise, name='maj_tuteur_entreprise'),
]
