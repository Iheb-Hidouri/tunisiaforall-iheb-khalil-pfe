from django.db import models

class Adherent(models.Model):
    numero_adherent = models.CharField(max_length=8, unique=True)
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
    document_identite = models.CharField(max_length=2, choices=DOCUMENT_IDENTITE_CHOICES)
    numero_document_identite = models.CharField(max_length=8)
    date_delivrance_ci = models.DateField(null=True, blank=True)
    date_validite_cs = models.DateField(null=True, blank=True)
    nationalite = models.CharField(max_length=50)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    rue = models.CharField(max_length=20)
    cite_quartier = models.CharField(max_length=20)
    ville = models.CharField(max_length=15)
    code_postal = models.CharField(max_length=4)
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
    derniere_cotisation_payee = models.CharField(max_length=4)
    date_reglement_cotisation = models.DateField()
    date_adhesion = models.DateField()
    date_depart = models.DateField(null=True, blank=True)
    motif_depart = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.numero_adherent

    

class Structure(models.Model):
    code_stucture = models.CharField(max_length=6)
    libelle = models.CharField(max_length=20)
    rue = models.CharField(max_length=20)
    cite_quartier = models.CharField(max_length=15)
    ville = models.CharField(max_length=15)
    code_postal = models.CharField(max_length=4)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    date_creation = models.DateField()
    date_ag = models.DateField()
    
    def __str__(self):
       return self.code

    
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