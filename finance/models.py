from django.db import models
from base.models import Structure , Adherent , Evenement

class BanqueTransactions(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE ,null=True, blank=True)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE ,null=True, blank=True)
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE ,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    entreprise = models.CharField(max_length=50)
    libelle = models.CharField(max_length=50)
    banque = models.CharField(max_length=50)
    cheque_numero = models.CharField(max_length=20)
    debit = models.BooleanField(default=False)
    credit = models.BooleanField(default=False)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    justificatif_banque = models.ImageField( null=True, blank=True)
        
class CaisseTransactions(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE ,null=True, blank=True)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE ,null=True, blank=True)
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE ,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    entreprise = models.CharField(max_length=50)
    libelle = models.CharField(max_length=50)
    recu_numero = models.CharField(max_length=20)
    debit = models.BooleanField(default=False)
    credit = models.BooleanField(default=False)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    justificatif_caisse = models.ImageField( null=True, blank=True)