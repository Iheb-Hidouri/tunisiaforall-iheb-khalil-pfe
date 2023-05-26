from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver



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
    exclude_fields = ['date_creation', 'date_ag']

    @receiver(pre_save, sender='base.Structure')
    def pre_save_structure(sender, instance, **kwargs):
        if instance.pk:
            original_instance = Structure.objects.get(pk=instance.pk)
            instance._changes = original_instance.get_changes(instance)
            
    def get_changes(self, new_instance):
        changes = []
        
        for field in self._meta.fields:
          if field.name not in self.exclude_fields:  
            old_value = getattr(self, field.name)
            new_value = getattr(new_instance, field.name)
            if old_value != new_value:
                change = f"{field.name}: {old_value} ----> {new_value}"
                changes.append(change)
        return changes
    
    
    def __str__(self):
       return self.code_structure


class Adherent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='adherent')
    code = models.CharField(max_length=8)
    image= models.ImageField(upload_to='img/',null=True, blank=True)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE , related_name='adherents', default = 1)
   
    TYPE_ADHERENT_CHOICES = (
    ('Membre fondateur', 'Membre fondateur'),
    ('Membre actif', 'Membre actif'),
    ('Membre actif jeune', 'Membre actif jeune'),
    ('Soutien', 'Soutien'),
    ('Président', 'Président'),
    ('Directeur Executif', 'Directeur Executif'),
    ('Trésorier', 'Trésorier'),
    ('Simple membre', 'Simple membre'),
    )
    
    type_adherent = models.CharField(max_length=20, choices=TYPE_ADHERENT_CHOICES)
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
    type_document_identite = models.CharField(max_length=2, choices=DOCUMENT_IDENTITE_CHOICES,null=True)

    numero_document_identite = models.CharField(max_length=8)
    
    
    nationalite = models.CharField(max_length=50)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    
    telephone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    COMMISSION_CHOICES = (
        ('Enseignement, Sciences et Technologies', 'Enseignement, Sciences et Technologies'),
        ('Développement et emploi', 'Développement et emploi'),
        ('Santé et social', 'Santé et social'),
        ('Culture, tourisme et environnement', 'Culture, tourisme et environnement'),
        ('Autre', 'Autre'),
    )
    commissions = models.CharField(max_length=(50), choices=COMMISSION_CHOICES,null=True,blank=True)
    date_adhesion = models.DateField(blank=True, null=True)
    date_depart = models.DateField(null=True, blank=True)
    motif_depart = models.CharField(max_length=50, null=True, blank=True)
    cotisation_annuelle = models.CharField(max_length=50, default='non payée')
    exclude_fields = ['date_adhesion', 'date_naissance']

    @receiver(pre_save, sender='base.Adherent')
    def pre_save_adherent(sender, instance, **kwargs):
        if instance.pk:
            original_instance = Adherent.objects.get(pk=instance.pk)
            instance._changes = original_instance.get_changes(instance)
            
    def get_changes(self, new_instance):
        changes = []
        
        for field in self._meta.fields:
          if field.name not in self.exclude_fields:  
            old_value = getattr(self, field.name)
            new_value = getattr(new_instance, field.name)
            if old_value != new_value:
                change = f"{field.name}: {old_value} ----> {new_value}"
                changes.append(change)
        return changes
    def __str__(self):
        return self.code
    
    
class AdherentHistory(models.Model):
    user = models.CharField(max_length=20,blank=True, null=True)
    adherent = models.CharField(max_length=20,blank=True, null=True)
    action = models.CharField(max_length=10)
    changes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Adherent: {self.adherent}, Action: {self.action}"

class StructureHistory(models.Model):
    user = models.CharField(max_length=20,blank=True, null=True)
    structure = models.CharField(max_length=20,blank=True, null=True)
    action = models.CharField(max_length=10)
    changes = models.TextField(blank=True, null=True)
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
    
class BanqueTransactions(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE ,null=True, blank=True)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE ,null=True, blank=True)
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE ,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    entreprise = models.CharField(max_length=50)
    libelle = models.CharField(max_length=50)
    banque = models.CharField(max_length=50)
    cheque_numero = models.CharField(max_length=20)
    TRANSACTION_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_CHOICES)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    justificatif_banque = models.ImageField( null=True, blank=True)
    REASON_CHOICES = (
        ('don', 'Don'),
        ('cotisation', 'Cotisation'),
        ('frais', 'Frais'),
        ('profits', 'profits'),
        
    )
    transaction_raison = models.CharField(max_length=20, choices=REASON_CHOICES, default='don')
     
        
class CaisseTransactions(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE ,null=True, blank=True)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE ,null=True, blank=True)
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE ,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    entreprise = models.CharField(max_length=50)
    libelle = models.CharField(max_length=50)
    recu_numero = models.CharField(max_length=20)
    TRANSACTION_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_CHOICES)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    justificatif_caisse = models.ImageField( null=True, blank=True) 
    REASON_CHOICES = (
        ('don', 'Don'),
        ('cotisation', 'Cotisation'),
        ('frais', 'Frais'),
        ('profits', 'profits'),
        
    )
    transaction_raison = models.CharField(max_length=20,choices= REASON_CHOICES, default='don')


class CaisseTransactionHistory(models.Model):
    user = models.CharField(max_length=20,blank=True, null=True)
    caisse_transaction = models.CharField(max_length=20,blank=True, null=True)
    action = models.CharField(max_length=10)
    old_data = models.TextField(blank=True, null=True)
    new_data = models.TextField(blank=True, null=True, default='nothing')
    timestamp = models.DateTimeField(default=timezone.now)    


class BanqueTransactionHistory(models.Model):
    user = models.CharField(max_length=20,blank=True, null=True)
    banque_transaction = models.CharField(max_length=20,blank=True, null=True)
    action = models.CharField(max_length=10)
    old_data = models.TextField(blank=True, null=True)
    new_data = models.TextField(blank=True, null=True, default='nothing')
    timestamp = models.DateTimeField(default=timezone.now)     

class Cotisation(models.Model):
    ADHERENT_CHOICES = (
        ('B', 'Bank'),
        ('C', 'Caisse'),
    )
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    cotisation_type = models.CharField(max_length=1, choices=ADHERENT_CHOICES)
    number = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    entreprise = models.CharField(max_length=50)
    libelle = models.CharField(max_length=50)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    justificatif = models.ImageField(null=True, blank=True)    

