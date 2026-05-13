from django.db import models


class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    site_web = models.URLField(blank=True)
    description = models.TextField(blank=True)
    secteur = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Offre(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    competences = models.TextField(blank=True, null=True)  
    formation = models.TextField(blank=True, null=True)     
    qualites = models.TextField(blank=True, null=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.titre


class Candidature(models.Model):
    nom_stagiaire = models.CharField(max_length=150)

    # ✅ نخليهم null/blank باش migration تدوز بلا default (حيت كاينين سجلات قدام)
    prenom_stagiaire = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=30, null=True, blank=True)

    # ✅ CV upload
    cv = models.FileField(upload_to="cvs/", null=True, blank=True)

    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date_candidature = models.DateTimeField(auto_now_add=True)

    # ==========================================================
    # 🌟 HNA ZEDNA SCORE IA W STATUT (BACHI L'CONVENTION T-KHDEM)
    # ==========================================================
    score_ia = models.FloatField(null=True, blank=True)

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTEE', 'Acceptée'),
        ('REFUSEE', 'Refusée'),
    ]
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='EN_ATTENTE'
    )
    # ==========================================================

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["offre", "nom_stagiaire", "prenom_stagiaire"],
                name="unique_candidature_par_offre"
            )
        ]

    def __str__(self):
        prenom = self.prenom_stagiaire or ""
        return f"{self.nom_stagiaire} {prenom} → {self.offre}"

class StageActif(models.Model):
    candidature = models.OneToOneField(Candidature, on_delete=models.CASCADE, limit_choices_to={'statut': 'ACCEPTEE'}, related_name='stage_actif')
    encadrant = models.ForeignKey('pages.Encadrant', on_delete=models.SET_NULL, null=True, blank=True, related_name='stages_supervises')

    # Tuteur côté entreprise
    tuteur_entreprise_nom  = models.CharField(max_length=150, blank=True, null=True)
    tuteur_entreprise_email = models.EmailField(blank=True, null=True)

    date_debut_effective = models.DateField(null=True, blank=True)
    date_fin_effective   = models.DateField(null=True, blank=True)

    # Dépôt rapport (legacy – on garde pour compatibilité)
    rapport_file = models.FileField(upload_to="rapports/", null=True, blank=True)

    # Validation pédagogique du sujet (section 3.4)
    sujet_valide = models.BooleanField(default=False)

    # Évaluations & feedbacks
    evaluation_encadrant = models.TextField(blank=True, null=True, help_text="Évaluation académique de l'encadrant")
    feedback_entreprise  = models.TextField(blank=True, null=True, help_text="Feedback de l'encadrant professionnel")
    
    # Détails évaluation entreprise (Bilan de fin de stage)
    note_assiduite = models.IntegerField(default=0, help_text="Note sur 5")
    note_technique = models.IntegerField(default=0, help_text="Note sur 5")
    note_integration = models.IntegerField(default=0, help_text="Note sur 5")
    
    remarques_encadrant  = models.TextField(blank=True, null=True, help_text="Directives / remarques visibles par l'étudiant")
    note_finale = models.FloatField(null=True, blank=True)

    STATUT_STAGE_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('TERMINE',  'Terminé'),
        ('ANNULE',   'Annulé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_STAGE_CHOICES, default='EN_COURS')

    date_creation    = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stage : {self.candidature.nom_stagiaire} - {self.candidature.offre.titre}"


class Livrable(models.Model):
    """Fichiers déposés par le stagiaire (rapports d'étape, rapport final, attestation…)."""

    TYPE_CHOICES = [
        ('AVANCEMENT', "Rapport d'avancement"),
        ('FINAL',      'Rapport final PFE'),
        ('ATTESTATION','Attestation de stage'),
        ('AUTRE',      'Autre document'),
    ]

    stage        = models.ForeignKey(StageActif, on_delete=models.CASCADE, related_name='livrables')
    type_doc     = models.CharField(max_length=20, choices=TYPE_CHOICES, default='AVANCEMENT')
    fichier      = models.FileField(upload_to='livrables/')
    date_depot   = models.DateTimeField(auto_now_add=True)
    telecharge   = models.BooleanField(default=False, help_text="Marqué True lorsque l'encadrant télécharge le fichier")

    def nom_fichier(self):
        return self.fichier.name.split('/')[-1]

    def __str__(self):
        return f"{self.get_type_doc_display()} — {self.stage}"
