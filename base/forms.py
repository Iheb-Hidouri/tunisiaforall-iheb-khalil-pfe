from django import forms
from django.forms import ModelForm
from .models import Adherent , Structure , User,  Cotisation
from django.utils import timezone
from .models import BanqueTransactions, CaisseTransactions
from django.forms import ClearableFileInput
from datetime import date
from django.utils.translation import gettext_lazy as _




class AdherentForm(ModelForm):
    pseudo = forms.CharField(max_length=30)
    mot_de_passe = forms.CharField(max_length=30, widget=forms.PasswordInput)
    confirmer_le_mot_de_passe = forms.CharField(max_length=30, widget=forms.PasswordInput)
    class Meta:
        model = Adherent
        exclude = ['code','user', 'cotisation_annuelle','date_depart','motif_depart','dernière_date_de_payement'] # exclude the 'code' field from the form
        widgets = {
            'date_de_naissance': forms.DateInput({'type': 'date', 'lang': 'fr', 'format': '%d/%m/%Y'}),
            'date_émission_de_la_carte': forms.DateInput({'type': 'date', 'lang': 'fr', 'format': '%d/%m/%Y'}),
            'date_adhésion': forms.widgets.HiddenInput(),
            'photo_de_profile': ClearableFileInput()
            
        }
    def __init__(self, *args, **kwargs):
        user_structure = kwargs.pop('user_structure', None)
        super().__init__(*args, **kwargs)
        self.fields['structure'].disabled = True
        if user_structure:
            self.fields['structure'].initial = user_structure   
       
        self.fields['mot_de_passe'].required = True
        self.fields['confirmer_le_mot_de_passe'].required = True
        self.fields['nationalité'].required = True
        self.fields['profession'].required = True
        self.fields['numéro_de_téléphone'].required = True
        self.fields['adresse_email'].required = True
        self.fields['date_émission_de_la_carte'].required = True
        
            
    def clean(self):
        cleaned_data = super().clean()
        pseudo = cleaned_data.get('pseudo')
        if User.objects.filter(username=pseudo).exists():
            self.add_error('pseudo', "Ce pseudo est déjà utilisé.")
        password = cleaned_data.get('mot_de_passe')
        confirm_password = cleaned_data.get('confirmer_le_mot_de_passe')
        if password != confirm_password:
            raise forms.ValidationError("Les deux champs de mot de passe ne correspondent pas.")
        date_de_naissance = cleaned_data.get('date_de_naissance')
        max_date = date(date.today().year - 18, 12, 31)  # Calculate the maximum allowed date (18 years ago)
        if date_de_naissance and date_de_naissance > max_date:
            self.add_error('date_de_naissance', "l'âge minimum d'un adhérent est 18 ans .")
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Autogenerate the code for the new Adherent object
        last_code = Adherent.objects.order_by('-code').values_list('code', flat=True).first() # get the last 'code' value from the Adherent model
        last_count = int(last_code.split('-')[0]) if last_code else 0 # extract the count from the last 'code' value if it exists, otherwise set it to 0
        structure_code = instance.structure.code_structure.split('-')[1]
        if instance.type_adhérent == 'Membre fondateur':
                code = f"{last_count+1:04d}-0000"   
        else :            # extract the last 4 digits of the 'code_structure' value from the associated Structure object
                code = f"{last_count+1:04d}-{structure_code[-4:]}" # construct the new 'code' value for the Adherent object
        instance.code = code # set the 'code' field for the new Adherent object to the generated value
        # Set the 'date_adhesion' field for the new Adherent object to the current time
        instance.date_adhésion = timezone.now()
        if commit:
            # Create the user for the new Adherent object
            user = User.objects.create_user(
            username=self.cleaned_data['pseudo'], 
            password=self.cleaned_data['mot_de_passe']
        )
            instance.user = user
            instance.save() # save the new Adherent object to the database
        return instance
    
    
class UpdateAdherentForm(ModelForm):
     class Meta:
        model = Adherent
        exclude = ['code', 'user','cotisation_annuelle','date_depart','motif_depart','dernière_date_de_payement']
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date', 'lang': 'fr'}),
            'date_émission_de_la_carte': forms.DateInput({'type': 'date', 'lang': 'fr', 'format': '%d/%m/%Y'}),
            'date_adhésion': forms.widgets.HiddenInput(),
        }
    
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['structure'].queryset = Structure.objects.all()
        self.fields['nationalité'].required = True
        self.fields['profession'].required = True
        self.fields['numéro_de_téléphone'].required = True
        self.fields['adresse_email'].required = True

     def clean_date_de_naissance(self):
        date_de_naissance = self.cleaned_data['date_de_naissance']
        max_date = date(date.today().year - 18, 12, 31)  # Calculate the maximum allowed date (18 years ago)
        if date_de_naissance > max_date:
            raise forms.ValidationError("Date de naissance must be on or before 2005.")
        return date_de_naissance   
    
     def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class StructureForm(ModelForm):
    class Meta:
        model= Structure
        fields= [
            'type',
            'gouvernorat',
            'délégation',
            'adresse',
            'code_postal',
            'numéro_de_téléphone',
            'adresse_email',
            'date_de_création',
            'date_AG'
        ] 
        widgets = {
            'date_de_création': forms.DateInput(attrs={'type': 'date'}),
            'date_AG': forms.DateInput(attrs={'type': 'date'}),
        }  # include these fields in the form for the Structure model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
            
    def save(self, commit=True):
        instance = super().save(commit=False)
        code_structure = f"{instance.type}-{instance.gouvernorat.code}{instance.délégation.code}"
             # construct a new 'code_structure' value based on the 'type', 'governat', and 'delegation' fields
        instance.code_structure = code_structure
        libellé=f"{instance.type}-{instance.délégation.name}"
        instance.libellé= libellé
            # set the 'code_structure' field for the new Structure object to the generated value
        if commit:
            instance.save() # save the new Structure object to the database
        return instance  



class BanqueTransactionsForm(forms.ModelForm):
    class Meta:
        model = BanqueTransactions
        exclude = ['libellé']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        user_structure = kwargs.pop('user_structure', None)
        super().__init__(*args, **kwargs)
        self.fields['structure'].disabled = True  
        if user_structure:
            self.fields['structure'].initial = user_structure 
    def save(self, commit=True):
        instance = super().save(commit=False)
        libelle = f"{instance.structure}-{instance.raison_de_transaction}"
        if instance.adhérent:
            libelle += f"-{instance.adhérent}"
        elif instance.évènement:
            libelle += f"-{instance.évènement}"
        instance.libellé = libelle
        if commit:
            instance.save()
        return instance     

class CaisseTransactionsForm(forms.ModelForm):
    class Meta:
        model = CaisseTransactions
        exclude = ['libellé']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }  

    def __init__(self, *args, **kwargs):
        user_structure = kwargs.pop('user_structure', None)
        super().__init__(*args, **kwargs)
        self.fields['structure'].disabled = True  
        if user_structure:
            self.fields['structure'].initial = user_structure 

    def save(self, commit=True):
        instance = super().save(commit=False)
        libelle = f"{instance.structure}-{instance.raison_de_transaction}"
        if instance.adhérent:
            libelle += f"-{instance.adhérent}"
        elif instance.évènement:
            libelle += f"-{instance.évènement}"
        
        instance.libellé = libelle
        if commit:
            instance.save()
        return instance
      
           

class CotisationPaymentForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ['moyen_de_payement', 'numéro_chèque_ou_recu', 'date', 'entreprise', 'libellé', 'solde', 'justificatif']                  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }     