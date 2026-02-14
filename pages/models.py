from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('ETUDIANT', 'Etudiant'),
        ('ENTREPRISE', 'Entreprise'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'ETUDIANT'})
    cne = models.CharField(max_length=20)
    filiere = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

class Entreprise(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='entreprise')
   nom_societe = models.CharField(max_length=100)
   secteur = models.CharField(max_length=100)
   ville = models.CharField(max_length=50)
   description = models.TextField(blank=True)
   site_web = models.URLField(blank=True)

   def __str__(self):
        return self.nom_societe
   