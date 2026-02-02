from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Bach n-ferqo bin l-étudiant w l-prof
    is_stagiaire = models.BooleanField(default=False)
    is_encadrant = models.BooleanField(default=False)

class Stagiaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cne = models.CharField(max_length=20)
    filiere = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)

