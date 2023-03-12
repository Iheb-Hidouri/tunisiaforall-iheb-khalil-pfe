from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
from django.db import models

class Adherent(models.Model):
    code_adherent = models.CharField(primary_key=True, max_length=1)
    code_struct_adherent = models.CharField(max_length=5)
    nom_adherent = models.CharField(max_length=100)
    prenom_adherent = models.CharField(max_length=100)
    nation_adherent = models.CharField(max_length=50)
    tel_adherent = models.CharField(max_length=20)
    email_adherent = models.EmailField(max_length=100)
    type_adherent = models.IntegerField()
    date_naissance_adherent = models.DateField()
    photo_adherent = models.CharField(max_length=100)
    Date_sai =  models.DateField()
    login_adherent = models.EmailField(max_length=100)
    mdp_adherent = models.EmailField(max_length=20)
    observations_adherent =  models.CharField(max_length=100)
    cin_adherent= models.CharField(max_length=10)
    genre_adherent= models.CharField(max_length=10 , choices=[('M', 'Masculin'), ('F', 'Féminin')])
    lieu_nais_adherent =  models.CharField(max_length=50)
    profession_adherent =  models.CharField(max_length=50)
    secteur_adherent = models.CharField(max_length=50)
    date_adhesion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_adherent} {self.prenom_adherent}"
    

class HistoriqueAdherent(models.Model):
    id_historique_client = models.AutoField(primary_key=True)
    code_adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    date_modification = models.DateTimeField(auto_now_add=True)
    modifie_par = models.CharField(max_length=100)
    type_modif = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_historique_client}: {self.code_adherent.code_adherent}"
    

class StructureAssociation(models.Model):
    code_struct = models.CharField(primary_key=True, max_length=10)
    gouv_structure = models.CharField(max_length=50)
    delegstruct = models.CharField(max_length=50)
    date_crea = models.DateField()
    type_struct = models.CharField(max_length=50)
    matricule_fiscale = models.CharField(max_length=50)
    JORT_crea = models.CharField(max_length=50)
    nro_cpt_ban = models.CharField(max_length=50)
    code_president = models.CharField(max_length=10)
    code_vice = models.CharField(max_length=10)
    code_direxe = models.CharField(max_length=10)
    code_tresor = models.CharField(max_length=10)
    code_membre = models.CharField(max_length=10)

    def __str__(self):
        return self.code_struct


class HistoriqueStructure(models.Model):
    id_historique_struct = models.AutoField(primary_key=True)
    code_struct = models.ForeignKey(StructureAssociation, on_delete=models.CASCADE)
    date_modif_struct = models.DateTimeField(auto_now_add=True)
    struct_modifie_par = models.CharField(max_length=50)
    type_modif_struct = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id_historique_struct} - {self.code_struct}"

    