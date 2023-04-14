from django import forms
from django.forms import ModelForm
from .models import Adherent , Structure , Governat , Delegation


class AdherentForm(ModelForm):
    class Meta:
        model = Adherent
        exclude = ['code'] # exclude the 'code' field from the form
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['structure'].queryset = Structure.objects.all() # set the queryset for the 'structure' field to all Structure objects
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Autogenerate the code for the new Adherent object
        last_code = Adherent.objects.order_by('-code').values_list('code', flat=True).first() # get the last 'code' value from the Adherent model
        last_count = int(last_code.split('-')[0]) if last_code else 0 # extract the count from the last 'code' value if it exists, otherwise set it to 0
        structure_code = instance.structure.code_structure.split('-')[1] # extract the last 4 digits of the 'code_structure' value from the associated Structure object
        code = f"{last_count+1:04d}-{structure_code[-4:]}" # construct the new 'code' value for the Adherent object
        
        instance.code = code # set the 'code' field for the new Adherent object to the generated value
        
        if commit:
            instance.save() # save the new Adherent object to the database
        return instance


class StructureForm(ModelForm):
    governat = forms.ModelChoiceField(queryset=Governat.objects.all(), empty_label=None) # create a ModelChoiceField for the 'governat' field with all available Governat objects
    delegation = forms.ModelChoiceField(queryset=Delegation.objects.all(), empty_label=None) # create a ModelChoiceField for the 'delegation' field with all available Delegation objects
    class Meta:
        model= Structure
        fields= [
            'type',
            'libelle',
            'rue',
            'governat',
            'delegation',
            'code_postal',
            'telephone',
            'email',
            'date_creation',
            'date_ag'
        ]   # include these fields in the form for the Structure model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['delegation'].queryset = Delegation.objects.filter(governat=self.instance.governat) 
        else :
            governat_id = self.initial.get('governat', None)
            if governat_id:
             self.fields['delegation'].queryset = Delegation.objects.filter(governat_id=governat_id) # set the queryset for the 'delegation' field based on the selected 'governat' value, if one exists
            
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.code_structure:
            code_structure = f"{instance.type}-{instance.governat.code}{instance.delegation.code}" # construct a new 'code_structure' value based on the 'type', 'governat', and 'delegation' fields
            instance.code_structure = code_structure # set the 'code_structure' field for the new Structure object to the generated value
        if commit:
            instance.save() # save the new Structure object to the database
        return instance             