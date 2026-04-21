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
