from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator



def validate_eight_digits(value):
    if not str(value).isdigit() or len(str(value)) != 8:
        raise ValidationError('Le numéro de la carte d\'identité doit être 8 chiffres.')    

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
  
    TYPE_CHOICES = [
        ('BN', 'Bureau National'),
        ('BR', 'Bureau regional'),
        ('BL', 'Bureau Local'),
        ('PR', 'Projet'),
    ]

    code_structure = models.CharField(max_length=6)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    libellé = models.CharField(max_length=20)
    adresse = models.CharField(max_length=20)
    gouvernorat = models.ForeignKey(Governat, on_delete=models.CASCADE , related_name='structures')
    délégation = models.ForeignKey(Delegation, on_delete=models.CASCADE , related_name='structures')
    code_postal = models.CharField(max_length=4)
    numéro_de_téléphone = models.CharField(max_length=20)
    adresse_email = models.EmailField()
    date_de_création = models.DateField()
    date_AG = models.DateField()
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
                change = f"{field.name}: ==> {new_value}"
                changes.append(change)
        return '  /  '.join(changes)
    
    
    def __str__(self):
       return self.code_structure
    


class Adherent(models.Model):
    TYPE_ADHERENT_CHOICES = (
    ('Membre fondateur', 'Membre fondateur'),
    ('Membre actif', 'Membre actif'),
    ('Membre actif jeune', 'Membre actif jeune'),
    ('Soutien', 'Soutien'),
    ('Membre d\'honneur ', 'Membre d\'honneur '),
    )
    RESPONSABILTE_ADHERENT_CHOICES = (
    ('Président', 'Président'),
    ('Viceprésident', 'Vice président'),
    ('Directeur Executif', 'Directeur Executif'),
    ('Trésorier', 'Trésorier'),
    ('Trésorier adjoint ', 'Trésorier adjoint '),
    ('Chef Projet', 'Chef Projet'),
    ('Coordinateur de commission ', 'Coordinateur de commission '),
    ('Membre Simple ', 'Membre Simple '),
    )
    GENRE_CHOICES = (
        ('M', 'M'),
        ('F', 'F'),
    )
    DOCUMENT_IDENTITE_CHOICES = (
        ('CIN', 'Carte d\'identité'),
        ('CS', 'Carte de séjour'),
    )
    COMMISSION_CHOICES = (
        ('Enseignement, Sciences et Technologies', 'Enseignement, Sciences et Technologies'),
        ('Développement et emploi', 'Développement et emploi'),
        ('Santé et social', 'Santé et social'),
        ('Culture, tourisme et environnement', 'Culture, tourisme et environnement'),
        ('Autre', 'Autre'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='adherent')
    code = models.CharField(max_length=9)
    photo_de_profile= models.ImageField(upload_to='img/',null=True, blank=True,default='img/navbar_logo.png')
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE , related_name='adherents', default = 1)
    type_adhérent = models.CharField(max_length=27, choices=TYPE_ADHERENT_CHOICES)
    responsabilité_adhérent= models.CharField(max_length=27, choices=RESPONSABILTE_ADHERENT_CHOICES, null=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    nom = models.CharField(max_length=50)
    prénom = models.CharField(max_length=50)
    type_document_identité = models.CharField(max_length=3, choices=DOCUMENT_IDENTITE_CHOICES,null=True)
    numero_document_identité = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99999999),
        validate_eight_digits
    ])
    date_émission_de_la_carte = models.DateField(null=True, blank=True)
    nationalité = models.CharField(max_length=50)
    date_de_naissance = models.DateField()
    lieu_de_naissance = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    numéro_de_téléphone = models.CharField(max_length=20)
    adresse_email = models.EmailField(max_length=50)
    commissions = models.CharField(max_length=(50), choices=COMMISSION_CHOICES,null=True,blank=True)
    date_adhésion = models.DateField(blank=True, null=True)
    date_depart = models.DateField(null=True, blank=True)
    motif_depart = models.CharField(max_length=50, null=True, blank=True)
    cotisation_annuelle = models.CharField(max_length=50, default='non payée')
    dernière_date_de_payement = models.DateField(null=True, blank=True)
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
                change = f"{field.name}: ==> {new_value}"
                changes.append(change)
     
     return '  /  '.join(changes)
    def __str__(self):
        return self.code
    
    
class History(models.Model):
    user = models.CharField(max_length=20, blank=True, null=True)
    action = models.CharField(max_length=10)
    changes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class AdherentHistory(History):
    adherent = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Adherent: {self.adherent}, Action: {self.action}"

class StructureHistory(History):
    structure = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Structure: {self.structure}, Action: {self.action}" 



        
class ResponsableStructure(models.Model):
    code_structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    numero_adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    responsabilite = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.code_adherent} - {self.code_structure} ({self.responsabilite})"


class Evenement(models.Model):
    TYPE_CHOICES = (
        (1, 'Bureau Exécutif'),
        (2, 'Commission'),
        (3, 'AG'),
        (4, 'Conférence'),
        (5, 'Activité'),
    )
    initiateur = models.ForeignKey(Structure, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    libelle = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPE_CHOICES)
    date_debut = models.DateField()
    heure_debut = models.TimeField()
    date_fin = models.DateField()
    heure_fin = models.TimeField()
    lieu = models.CharField(max_length=255)
    partenaires = models.ManyToManyField(Structure, related_name='evenements_partenaires', blank=True)
    membres_invites = models.ManyToManyField(Adherent, related_name='evenements_membres_invites', blank=True)

    def __str__(self):
        return f"{self.libelle} ({self.get_type_display()}) "
    
class Transaction(models.Model):
    REASON_CHOICES = (
        ('Don', 'Don'),
        ('Cotisation', 'Cotisation'),
        ('Aide financier','Aide financier'),
        ('Dépenses sur évènement ', 'Dépenses sur évènement '),
        ('Recette d\'évènement ', 'Recette d\'évènement'),
    )
    TRANSACTION_CHOICES = (
        ('Crédit', 'Crédit'),
        ('Débit', 'Débit'),
    )
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE,null=True, blank=True )
    évènement = models.ForeignKey(Evenement, on_delete=models.CASCADE, null=True, blank=True)
    adhérent = models.ForeignKey(Adherent, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    entreprise = models.CharField(max_length=50)
    libellé = models.CharField(max_length=50)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    type_de_transaction = models.CharField(max_length=6, choices=TRANSACTION_CHOICES)
    raison_de_transaction = models.CharField(max_length=23, choices=REASON_CHOICES, default='raison inconnue')
    source_transaction = models.CharField(max_length=20)
    
    class Meta:
        abstract = True

class BanqueTransactions(Transaction):
    banque = models.CharField(max_length=50)
    numéro_du_chèque = models.CharField(max_length=20)
    justificatif_bancaire = models.ImageField(upload_to='img/', null=True, blank=True)
    source_transaction = 'Bancaire'
    
    
class CaisseTransactions(Transaction):
    recu_numéro = models.CharField(max_length=20)
    justificatif_caisse = models.ImageField(upload_to='img/', null=True, blank=True)
    source_transaction = 'En liquide'
   

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
    timestamp = models.DateField(default=timezone.now)     

class Cotisation(models.Model):
    ADHERENT_CHOICES = (
        ('Banque', 'Banque'),
        ('Caisse', 'Caisse'),
    )
    adhérent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    moyen_de_payement = models.CharField(max_length=8, choices=ADHERENT_CHOICES,null=True)
    numéro_chèque_ou_recu = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    entreprise = models.CharField(max_length=50)
    libellé = models.CharField(max_length=50)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    justificatif = models.ImageField(upload_to='img/',null=True, blank=True)    

