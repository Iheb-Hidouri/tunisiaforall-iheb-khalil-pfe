from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Adherent, Structure , AdherentHistory
from .forms import AdherentForm , StructureForm
from django.db.models import Q
from .models import  Structure
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from auditlog.models import LogEntry
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User 
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from .signals import save_adherent_history, delete_adherent_history

def loginPage(request):
    if request.method == "POST" : 
        username =request.POST.get('username')
        password=request.POST.get('password')
        try :
            user = User.objects.get(username=username)
        except:
            messages.error(request , 'User does not exist') 
        user = authenticate(request , username=username , password=password)

        if user is not None :
            LogEntry.objects.create(
                user_id=user.id,
                content_type=ContentType.objects.get_for_model(User),
                object_id=user.id,
                object_repr=str(user),
                action_flag=ADDITION,
                change_message="User logged in",
            )
            login(request , user )    
            return redirect ('home') 
    context={}
    return render(request , 'base/login_register.html', context)
def logoutUser(request): 
    logout(request)
    return redirect  ('home')

def home (request) : 
    
    return render (request , 'base/home.html')

#VIEWS FOR ADHERENTS
def gestion_adherent(request):
    # Get the search query from the GET request parameters
    query = request.GET.get('q')
    if query:
        # If a search query is present, filter the list of adherents based on the query
        adherents = Adherent.objects.filter(
            Q(nom__icontains=query) | Q(prenom__icontains=query)
        )
    else:
        # If no search query is present, display all adherents
        adherents = Adherent.objects.all()
    # Create a dictionary with the adherents queryset and pass it to the template
    context = {'adherents': adherents}
    return render(request, 'base/gestion_adherent.html', context)

# This view displays a form for creating a new adherent
def create_adherent(request):
    # Create a new AdherentForm instance
    form = AdherentForm()
    
    if request.method == 'POST':
        # If the request method is POST, populate the form with the POST data
        form = AdherentForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the new adherent and redirect to the home page
            adherent = form.save(commit=False)
            
           
            adherent.user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            adherent.save()
            history = AdherentHistory.objects.get(adherent=adherent)
            history.user = request.user
            history.save()
           
            return redirect('home')
    # Create a dictionary with the form and pass it to the template
    context = {'form': form}
    return render(request, 'base/adherent_form.html', context)

# This view displays a form for updating an existing adherent
def update_adherent(request, pk):
    # Get the Adherent object with the given primary key
    adherent = Adherent.objects.get(id=pk)
    # Create a new AdherentForm instance and populate it with the Adherent data
    form = AdherentForm(instance=adherent)
    if request.method == 'POST':
        # If the request method is POST, populate the form with the POST data
        form = AdherentForm(request.POST, instance=adherent)
        if form.is_valid():
            # If the form is valid, save the updated adherent and redirect to the home page
            form.save()
           

            return redirect('home')
    # Create a dictionary with the form and the Adherent object and pass it to the template
    context = {'form': form, 'adherent': adherent}
    return render(request, 'base/adherent_form.html', context)

# This view deletes an existing adherent
def delete_adherent(request, pk):
    # Get the Adherent object with the given primary key
    adherent = Adherent.objects.get(id=pk)
    if request.method == 'POST':
        # If the request method is POST, delete the adherent and redirect to the list of adherents
        adherent.delete()
        return redirect('gestion_adherent')
    # Create a dictionary with the Adherent object and pass it to the template
    return render(request, 'base/delete.html', {'obj': adherent})

#VIEWS FOR STRUCTURES 
# This view displays a list of adherents and allows searching for specific adherents.
def gestion_structure (request) :
    query = request.GET.get('q')  # retrieve the search query from the request parameters
    if query:  # if there is a search query
        structures = Structure.objects.filter(  # retrieve structures that contain the search query in their code or label
            Q(code_structure__icontains=query) | Q(libelle__icontains=query)
        )
    else:  # if there is no search query
        structures = Structure.objects.all()  # retrieve all structures
    context = {'structures': structures}  # create a dictionary to store the structures and pass it to the view
    return render (request , 'base/gestion_structure.html', context)  # render the HTML template with the context data

# This view creates a new structure using a form.
def create_structure(request) : 
    form = StructureForm()  # create an empty form instance
    if request.method == 'POST' :  # if the user submits the form
        form=StructureForm(request.POST)  # create a form instance with the submitted data
        if form.is_valid() :  # if the form data is valid
           form.save()  # save the form data to the database
           return redirect('home')  # redirect the user to the home page
    context={'form':form}  # create a dictionary to store the form and pass it to the view
    return render(request , 'base/structure_form.html', context)  # render the HTML template with the context data

# This view updates an existing structure using a form.
def update_structure(request , pk) : 
    structure = Structure.objects.get(id=pk)  # retrieve the structure object with the given primary key
    form = StructureForm(instance=structure)  # create a form instance with the retrieved structure object as initial data
    if request.method == 'POST' :  # if the user submits the form
        form=StructureForm(request.POST , instance=structure)  # create a form instance with the submitted data and the retrieved structure object as initial data
        if form.is_valid():  # if the form data is valid
            form.save()  # save the form data to the database
            return redirect('home')  # redirect the user to the home page
    context={'form' : form , 'structure':structure}  # create a dictionary to store the form and structure and pass it to the view
    return render(request , 'base/structure_form.html', context)  # render the HTML template with the context data

# This view deletes an existing structure .
def delete_structure(request , pk) :
    structure= Structure.objects.get(id=pk)  # retrieve the structure object with the given primary key
    if request.method =='POST' :  # if the user confirms the delete action
        structure.delete()  # delete the structure object from the database
        return redirect('gestion_structure')  # redirect the user to the structure management page
    return render (request , 'base/delete.html', {'obj': structure})  # render the HTML template for delete confirmation with the context data



def adherent_history(request):
    history = AdherentHistory.objects.all().order_by('-timestamp')
    return render(request, 'base/adherent_history.html', {'history': history})






