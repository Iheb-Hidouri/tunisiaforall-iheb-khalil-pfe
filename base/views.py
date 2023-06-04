from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from .models import Adherent, Structure , AdherentHistory , StructureHistory , Cotisation , Delegation
from .forms import AdherentForm , StructureForm , UpdateAdherentForm
from django.db.models import Q
from .models import  Structure
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User 
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from .signals import  post_delete_adherent,post_save_adherent , post_save_structure, post_delete_structure, save_caisse_transaction_history,delete_caisse_transaction_history,save_banque_transaction_history,delete_banque_transaction_history
from django.forms.models import model_to_dict
from .forms import BanqueTransactionsForm, CaisseTransactionsForm , CotisationPaymentForm
from .models import BanqueTransactions, CaisseTransactions
from django.shortcuts import render
from django.db.models import Count
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Pseudo ou mot de passe invalide')

    return render(request, 'base/login_register.html')

def logoutUser(request): 
    logout(request)
    return redirect  ('home')

def home (request) : 
    
    return render (request , 'base/home.html')

#VIEWS FOR ADHERENTS
def gestion_adherent(request):
    # Get the search query from the GET request parameters
    if request.user.adherent.structure.code_structure == 'BN-1169' :
       adherents = Adherent.objects.all()
    else:   # If no search query is present, display all adherents
       adherents = Adherent.objects.filter(structure=request.user.adherent.structure)
    # Create a dictionary with the adherents queryset and pass it to the template
    context = {'adherents': adherents}
    return render(request, 'base/gestion_adherent.html', context)
def liste_adherent(request):
    # Get the search query from the GET request parameters
    
        # If no search query is present, display all adherents
    adherents = Adherent.objects.filter(structure=request.user.adherent.structure)
    # Create a dictionary with the adherents queryset and pass it to the template
    context = {'adherents': adherents}
    return render(request, 'base/liste_adherent.html', context)

# This view displays a form for creating a new adherent
def create_adherent(request):
    # Create a new AdherentForm instance
    form = AdherentForm()
    
    if request.method == 'POST':
        # If the request method is POST, populate the form with the POST data
        form = AdherentForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form is valid, save the new adherent and redirect to the home page
            adherent = form.save(commit=False)
            
           
            adherent.user = User.objects.create_user(
                username=form.cleaned_data['pseudo'],
                password=form.cleaned_data['mot_de_passe']
            )
            adherent.save()
            #SIGNAL
            
            post_save_adherent(sender=Adherent, instance=adherent, created=True, request=request)
            return redirect('gestion_adherent')
    # Create a dictionary with the form and pass it to the template
    context = {'form': form}
    return render(request, 'base/adherent_form.html', context)

# This view displays a form for updating an existing adherent
def update_adherent(request, pk):
    # Get the Adherent object with the given primary key
    adherent = Adherent.objects.get(id=pk)
    user = adherent.user
    # Create a new AdherentForm instance and populate it with the Adherent data
    form = UpdateAdherentForm(instance=adherent)
   
    if request.method == 'POST':
        # If the request method is POST, populate the form with the POST data
        form = UpdateAdherentForm(request.POST, request.FILES ,instance=adherent)
       
        if form.is_valid():
            adherent = form.save(commit=False)
            
            # If the form is valid, save the updated adherent and redirect to the home page
            form.save()
            
            #SIGNAL
            
            post_save_adherent(sender=Adherent, instance=adherent, created=False, request=request)
            return redirect('gestion_adherent')
    # Create a dictionary with the form and the Adherent object and pass it to the template
    context = {'form': form, 'adherent': adherent}
    return render(request, 'base/adherent_form.html', context)

# This view deletes an existing adherent
def delete_adherent(request, pk):
    # Get the Adherent object with the given primary key
    adherent = Adherent.objects.get(id=pk)
    if request.method == 'POST':
        
        
        # If the request method is POST, delete the adherent and redirect to the list of adherents
        adherent.user.delete()
        adherent.delete()
        post_delete_adherent(sender=Adherent, instance=adherent, request=request)
        return redirect('gestion_adherent')
    # Create a dictionary with the Adherent object and pass it to the template
    return render(request, 'base/delete.html', {'obj': adherent})

def consult_adherent(request, pk):
    # Get the Adherent object with the given primary key
    adherent = Adherent.objects.get(id=pk)
    
    # Create a dictionary with the Adherent object and pass it to the template
    return render(request, 'base/consult_adherent.html', {'adherent': adherent})

#VIEWS FOR STRUCTURES 
# This view displays a list of adherents and allows searching for specific adherents.
def gestion_structure (request) :
      # if there is no search query
    structures = Structure.objects.all()  # retrieve all structures
    context = {'structures': structures}  # create a dictionary to store the structures and pass it to the view
    return render (request , 'base/gestion_structure.html', context)
def liste_structure (request) :

     # if there is no search query
    structures = Structure.objects.all()  # retrieve all structures
    context = {'structures': structures}  # create a dictionary to store the structures and pass it to the view
    return render (request , 'base/liste_structure.html', context)   # render the HTML template with the context data

# This view creates a new structure using a form.
def create_structure(request) : 
    form = StructureForm()  # create an empty form instance
    if request.method == 'POST' :  # if the user submits the form
        form=StructureForm(request.POST)  # create a form instance with the submitted data
        if form.is_valid() :  # if the form data is valid
           structure=form.save()
           post_save_structure(sender=Structure, instance=structure, created=True, request=request)
           return redirect('gestion_structure')  # redirect the user to the home page
    context={'form':form}  # create a dictionary to store the form and pass it to the view
    return render(request , 'base/structure_form.html', context)  # render the HTML template with the context data

# This view updates an existing structure using a form.
def update_structure(request , pk) : 
    structure = Structure.objects.get(id=pk)  # retrieve the structure object with the given primary key
    form = StructureForm(instance=structure)  # create a form instance with the retrieved structure object as initial data
    if request.method == 'POST' :  # if the user submits the form
        form=StructureForm(request.POST , instance=structure)  # create a form instance with the submitted data and the retrieved structure object as initial data
        if form.is_valid():  # if the form data is valid
            structure = form.save()
            post_save_structure(sender=Structure, instance=structure, created=False, request=request)
            return redirect('gestion_structure')  # save the form data to the database
             # redirect the user to the home page
    context={'form' : form , 'structure':structure}  # create a dictionary to store the form and structure and pass it to the view
    return render(request , 'base/structure_form.html', context)  # render the HTML template with the context data

def delete_structure(request , pk) :
    structure= Structure.objects.get(id=pk)  # retrieve the structure object with the given primary key
    if request.method =='POST' :  # if the user confirms the delete action
        structure.delete()
        post_delete_structure(sender=Structure, instance=structure, request=request)  # delete the structure object from the database
        return redirect('gestion_structure')  # redirect the user to the structure management page
    return render (request , 'base/delete.html', {'obj': structure})  # render the HTML template for delete confirmation with the context data
def consult_structure(request, pk):
    # Get the Adherent object with the given primary key
    structure = Structure.objects.get(id=pk)
    
    # Create a dictionary with the Adherent object and pass it to the template
    return render(request, 'base/consult_structure.html', {'structure': structure})


def adherent_history(request):
    history = AdherentHistory.objects.all().order_by('-timestamp')
    return render(request, 'base/adherent_history.html', {'history': history})

def structure_history(request):
    history = StructureHistory.objects.all().order_by('-timestamp')
    return render(request, 'base/structure_history.html', {'history': history})


def gestion_financiere(request):
    # Get the search query from the GET request parameters
    if request.user.adherent.structure.code_structure == 'BN-1169':
        # If no search query is present, display all adherents
      banque_transactions = BanqueTransactions.objects.all() 
      caisse_transactions = CaisseTransactions.objects.all()

    # Combine the instances into a single list
      transactions = list(banque_transactions) + list(caisse_transactions)
    else :  
      banque_transactions = BanqueTransactions.objects.filter(structure=request.user.adherent.structure) 
      caisse_transactions = CaisseTransactions.objects.filter(structure=request.user.adherent.structure) 

    # Combine the instances into a single list
      transactions = list(banque_transactions) + list(caisse_transactions)

    # Pass the transactions to the template
    context = {'transactions': transactions }
    # Create a dictionary with the adherents queryset and pass it to the template
    
    return render(request, 'base/gestion_financiere.html', context)

def create_banque_transaction(request):
    if request.method == 'POST':
        form = BanqueTransactionsForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save()
            save_banque_transaction_history (sender=BanqueTransactions, instance=transaction,created=True, request=request)
            if transaction.raison_de_transaction == 'Cotisation':
                Cotisation.objects.create(
                    adhérent=transaction.adhérent,
                    moyen_de_payement='Banque',  # Assuming it represents a caisse transaction
                    numéro_chèque_ou_recu=transaction.numéro_du_chèque,
                    date=transaction.date,
                    entreprise=transaction.entreprise,
                    libellé=transaction.libellé,
                    solde=transaction.solde,
                    justificatif=transaction.justificatif_bancaire
                )
                adherent = transaction.adhérent
                adherent.cotisation_annuelle = 'payée'
                adherent.save()
            return redirect('gestion_financiere')  # Replace with your desired URL
    else:
        form = BanqueTransactionsForm()
    return render(request, 'base/banque_form.html', {'form': form})

def update_banque_transaction(request, pk):
    transaction = get_object_or_404(BanqueTransactions, id=pk)
    if request.method == 'POST':
        form = BanqueTransactionsForm(request.POST,request.FILES, instance=transaction)
        if form.is_valid():
            transaction =form.save()
            save_banque_transaction_history (sender=BanqueTransactions, instance=transaction,created=False, request=request)
            return redirect('gestion_financiere')  # Replace with your desired URL
    else:
        form = BanqueTransactionsForm(instance=transaction)
    return render(request, 'base/banque_form.html', {'form': form})

def consult_banque_transaction(request, pk):
    transaction = get_object_or_404(BanqueTransactions, id=pk)
    
    return render(request, 'base/consult_banque_transaction.html', {'transaction': transaction})

def consult_caisse_transaction(request, pk):
    transaction = get_object_or_404(CaisseTransactions, id=pk)
    
    return render(request, 'base/consult_caisse_transaction.html', {'transaction': transaction})

# Similar functions for CaisseTransactions
def create_caisse_transaction(request):
    if request.method == 'POST':
        form = CaisseTransactionsForm(request.POST, request.FILES)
        if form.is_valid():
            transaction=form.save()
            save_caisse_transaction_history (sender=CaisseTransactions, instance=transaction,created=True, request=request)
            if transaction.raison_de_transaction == 'Cotisation':
                Cotisation.objects.create(
                    adhérent=transaction.adhérent,
                    moyen_de_payement='Caisse',  # Assuming it represents a caisse transaction
                    numéro_chèque_ou_recu=transaction.recu_numéro,
                    date=transaction.date,
                    entreprise=transaction.entreprise,
                    libellé=transaction.libellé,
                    solde=transaction.solde,
                    justificatif=transaction.justificatif_caisse
                )
                adherent = transaction.adhérent
                adherent.cotisation_annuelle = 'payée'
                adherent.save()
            return redirect('gestion_financiere')  # Replace with your desired URL
    else:
        form = CaisseTransactionsForm()
    return render(request, 'base/caisse_form.html', {'form': form})

def update_caisse_transaction(request, pk):
    transaction = get_object_or_404(CaisseTransactions, id=pk)
    if request.method == 'POST':
        form = CaisseTransactionsForm(request.POST, request.FILES ,instance=transaction)
        
        if form.is_valid():
            form.save()
            save_caisse_transaction_history (sender=BanqueTransactions, instance=transaction,created=False, request=request)
            return redirect('gestion_financiere')  # Replace with your desired URL
    else:
        form = CaisseTransactionsForm(instance=transaction)
    return render(request, 'base/caisse_form.html', {'form': form})

def delete_banque_transaction(request, pk):
    transaction = get_object_or_404(BanqueTransactions, id=pk)
    
    if request.method == 'POST':
        if transaction.raison_de_transaction == 'Cotisation':
            Cotisation.objects.filter(adhérent=transaction.adhrent).delete()
        transaction.delete()
        adherent=transaction.adhérent
        adherent.cotisation_annuelle = 'non payée'
        adherent.save()
        delete_banque_transaction_history(sender=BanqueTransactions, instance=transaction, request=request) 
        # Perform any additional actions after deletion if needed
        return redirect('gestion_financiere')
    
    return render(request, 'base/delete.html', {'transaction': transaction})

def delete_caisse_transaction(request, pk):
    transaction = get_object_or_404(CaisseTransactions, id=pk)
    
    if request.method == 'POST':
        if transaction.raison_de_transaction == 'Cotisation':
            Cotisation.objects.filter(adhérent=transaction.adhérent).delete()
            
        transaction.delete()
        adherent=transaction.adhérent
        adherent.cotisation_annuelle = 'non payée'
        adherent.save()
        delete_banque_transaction_history(sender=CaisseTransactions, instance=transaction, request=request) 
        # Perform any additional actions after deletion if needed
        return redirect('gestion_financiere')
    
    return render(request, 'base/delete.html', {'transaction': transaction})

def payer_ma_cotisation(request):
    adherent = Adherent.objects.get(user=request.user)
    if request.method == 'POST':
        form = CotisationPaymentForm(request.POST ,  request.FILES)
        if form.is_valid():
            cotisation = form.save(commit=False)
            cotisation.adhérent = adherent
            cotisation.save()
            if cotisation.moyen_de_payement == 'Banque':
                BanqueTransactions.objects.create(
                    structure=adherent.structure,  # Add the relevant structure if necessary
                    évènement=None,  # Add the relevant event if necessary
                    adhérent=cotisation.adhérent,
                    date=cotisation.date,
                    entreprise=cotisation.entreprise,
                    libellé=cotisation.libellé,
                    banque='',  # Add the relevant bank information
                    numéro_du_chèque=cotisation.numéro_chèque_ou_recu,
                    solde=cotisation.solde,
                    justificatif_bancaire=cotisation.justificatif,
                    type_de_transaction='Crédit',
                    raison_de_transaction='Cotisation'
                )
            elif  cotisation.moyen_de_payement== 'Caisse':
                CaisseTransactions.objects.create(
                    structure=adherent.structure,  # Add the relevant structure if necessary
                    évènement=None,  # Add the relevant event if necessary
                    adhérent=cotisation.adhérent,
                    date=cotisation.date,
                    entreprise=cotisation.entreprise,
                    libellé=cotisation.libellé,
                    recu_numéro=cotisation.numéro_chèque_ou_recu,
                    solde=cotisation.solde,
                    justificatif_caisse=cotisation.justificatif,
                    type_de_transaction='Crédit',
                    raison_de_transaction='Cotisation'
                )
            adherent = cotisation.adhérent
            adherent.cotisation_annuelle = 'payée'
            adherent.save()    
            return redirect('profile')
    else:
        form = CotisationPaymentForm()
    return render(request, 'base/payer_ma_cotisation.html', {'form': form})

def profile(request):
    adherent = Adherent.objects.get(user=request.user)
    return render(request, 'base/profile.html', {'adherent': adherent})    

from django.http import JsonResponse
def fetch_delegations(request):
    governat_id = request.GET.get('gouvernorat_id')
    delegations = Delegation.objects.filter(governat_id=governat_id).values('id', 'name')
    return JsonResponse(list(delegations), safe=False)
import json
def adherents_view(request):
    count_male = Adherent.objects.filter(genre='M').count()
    count_female = Adherent.objects.filter(genre='F').count()
    # Perform other calculations or retrieve data from the Adherent model as needed

    gender_list = ['Male', 'Female']
    gender_number= [count_male, count_female]
    gender_labels_json = json.dumps(gender_list)
    gender_data_json = json.dumps(gender_number)

    # Add the JSON strings to the context
    context = {
        'gender_labels_json': gender_labels_json,
        'gender_data_json': gender_data_json,
    }
    # Prepare other data for charts if needed

    
    return render(request, 'base/dashboard.html', context)


