from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from auditlog.models import AuditlogHistoryField
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
import os
import uuid



class Governat(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Delegation(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)
    governat = models.ForeignKey(Governat, on_delete=models.CASCADE , related_name='delegations')

    def __str__(self):
        return self.name    

class Structure(models.Model):
    BN = 'BN'
    BR = 'BR'
    BL = 'BL'
    PR = 'PR'
    TYPE_CHOICES = [
        (BN, 'Bureau National'),
        (BR, 'Bureau regional'),
        (BL, 'Bureau Local'),
        (PR, 'Projet'),
    ]
    code_structure = models.CharField(max_length=6)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    libelle = models.CharField(max_length=20)
    rue = models.CharField(max_length=20)
    governat = models.ForeignKey(Governat, on_delete=models.CASCADE , related_name='structures')
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE , related_name='structures')
    code_postal = models.CharField(max_length=4)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    date_creation = models.DateField()
    date_ag = models.DateField()
   
    
    def __str__(self):
       return self.libelle


class Adherent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , default=None)
    code = models.CharField(max_length=8)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE , related_name='adherents', default = 1)
    TYPE_ADHERENT_CHOICES = (
        ('1', 'Membre fondateur'),
        ('2', 'Membre actif'),
        ('3', 'Membre actif jeune'),
        ('4', 'Soutien'),
        ('5', 'Membre d’honneur'),
    )
    type_adherent = models.CharField(max_length=1, choices=TYPE_ADHERENT_CHOICES)
    GENRE_CHOICES = (
        ('M', 'M.'),
        ('F', 'Mme.'),
    )
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    DOCUMENT_IDENTITE_CHOICES = (
        ('CI', 'Carte d\'identité'),
        ('CS', 'Carte de séjour'),
    )
    
    numero_document_identite = models.CharField(max_length=8)
    
    nationalite = models.CharField(max_length=50)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    
    telephone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    COMMISSION_CHOICES = (
        ('1', 'Enseignement, Sciences et Technologies'),
        ('2', 'Développement et emploi'),
        ('3', 'Santé et social'),
        ('4', 'Culture, tourisme et environnement'),
        ('5', 'Autre'),
    )
    commissions = models.CharField(max_length=5, choices=COMMISSION_CHOICES)
    date_adhesion = models.DateField(blank=True, null=True)
    date_depart = models.DateField(null=True, blank=True)
    motif_depart = models.CharField(max_length=50, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.nom
    
class AdherentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null=True)
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    action = models.CharField(max_length=10)
    old_data = models.TextField(blank=True, null=True)
    new_data = models.TextField(blank=True, null=True, default='nothing')
    timestamp = models.DateTimeField(default=timezone.now)

        
class ResponsableStructure(models.Model):
    code_structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    numero_adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    responsabilite = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.code_adherent} - {self.code_structure} ({self.responsabilite})"


class Evenement(models.Model):
    initiateur = models.ForeignKey(Structure, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    libelle = models.CharField(max_length=255)
    TYPE_CHOICES = (
        (1, 'Bureau Exécutif'),
        (2, 'Commission'),
        (3, 'AG'),
        (4, 'Conférence'),
        (5, 'Activité'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES)
    date_debut = models.DateField()
    heure_debut = models.TimeField()
    date_fin = models.DateField()
    heure_fin = models.TimeField()
    lieu = models.CharField(max_length=255)
    partenaires = models.ManyToManyField(Structure, related_name='evenements_partenaires', blank=True)
    membres_invites = models.ManyToManyField(Adherent, related_name='evenements_membres_invites', blank=True)

    def __str__(self):
        return f"{self.libelle} ({self.get_type_display()}) - {self.initiateur} ({self.date_debut} {self.heure_debut} - {self.date_fin} {self.heure_fin})"
    
