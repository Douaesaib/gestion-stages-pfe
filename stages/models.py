from django.db import models

class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    secteur = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Offre(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.titre


class Candidature(models.Model):
    nom_etudiant = models.CharField(max_length=150)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date_candidature = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_etudiant} → {self.offre}"

