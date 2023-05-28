from django import forms
from django.forms import ModelForm
from .models import Adherent , Structure , Governat ,User, Delegation , Cotisation
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from PIL import Image
from .models import BanqueTransactions, CaisseTransactions
from django.forms import ClearableFileInput
from django.forms.widgets import SelectDateWidget




class AdherentForm(ModelForm):
    pseudo = forms.CharField(max_length=30)
    mot_de_passe = forms.CharField(max_length=30, widget=forms.PasswordInput)
    confirmer_le_mot_de_passe = forms.CharField(max_length=30, widget=forms.PasswordInput)
    
    class Meta:
        model = Adherent
        exclude = ['code','user', 'cotisation_annuelle','date_depart','motif_depart'] # exclude the 'code' field from the form
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_adhésion': forms.widgets.HiddenInput(),
            
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['structure'].queryset = Structure.objects.all() # set the queryset for the 'structure' field to all Structure objects
        self.fields['mot_de_passe'].required = True
        self.fields['confirmer_le_mot_de_passe'].required = True
        self.fields['nationalité'].required = True
        self.fields['profession'].required = True
        self.fields['numéro_de_téléphone'].required = True
        self.fields['adresse_email'].required = True
        
            
    def clean(self):
        cleaned_data = super().clean()
       

        password = cleaned_data.get('mot_de_passe')
        confirm_password = cleaned_data.get('confirmer_le_mot_de_passe')

        if password != confirm_password:
            raise forms.ValidationError("The two password fields do not match.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Autogenerate the code for the new Adherent object
        last_code = Adherent.objects.order_by('-code').values_list('code', flat=True).first() # get the last 'code' value from the Adherent model
        last_count = int(last_code.split('-')[0]) if last_code else 0 # extract the count from the last 'code' value if it exists, otherwise set it to 0
        structure_code = instance.structure.code_structure.split('-')[1] # extract the last 4 digits of the 'code_structure' value from the associated Structure object
        code = f"{last_count+1:04d}-{structure_code[-4:]}" # construct the new 'code' value for the Adherent object
        
        instance.code = code # set the 'code' field for the new Adherent object to the generated value
        
       
       
        # Set the 'date_adhesion' field for the new Adherent object to the current time
        instance.date_adhesion = timezone.now()
        
        
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
        exclude = ['code', 'user','cotisation_annuelle','date_depart','motif_depart']
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_adhésion': forms.widgets.HiddenInput(),
            
        }
    
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['structure'].queryset = Structure.objects.all()
        self.fields['nationalité'].required = True
        self.fields['profession'].required = True
        self.fields['numéro_de_téléphone'].required = True
        self.fields['adresse_email'].required = True
    
     def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_adhesion = timezone.now()
        if commit:
            instance.save()
        return instance



class StructureForm(ModelForm):
    
    class Meta:
        model= Structure
        fields= [
            'type',
            'libellé',
            'rue',
            'gouvernorat',
            'délégation',
            'code_postal',
            'numéro_de_téléphone',
            'adresse_email',
            'date_de_création',
            'date_ag'
        ] 
        widgets = {
            'date_de_création': forms.DateInput(attrs={'type': 'date'}),
            'date_ag': forms.DateInput(attrs={'type': 'date'}),
        }  # include these fields in the form for the Structure model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
            
    def save(self, commit=True):
       
        instance = super().save(commit=False)
        
        if not instance.code_structure:
            code_structure = f"{instance.type}-{instance.governat.code}{instance.delegation.code}" # construct a new 'code_structure' value based on the 'type', 'governat', and 'delegation' fields
            instance.code_structure = code_structure # set the 'code_structure' field for the new Structure object to the generated value
        if commit:
            instance.save() # save the new Structure object to the database
        return instance  



class BanqueTransactionsForm(forms.ModelForm):
    class Meta:
        model = BanqueTransactions
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CaisseTransactionsForm(forms.ModelForm):
    class Meta:
        model = CaisseTransactions
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }     
class CotisationPaymentForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ['type_de_cotisation', 'numéro_chèque_ou_recu', 'date', 'entreprise', 'libellé', 'solde', 'justificatif']                  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }     