from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Adherent
from .forms import AdherentForm




def home (request) : 
    adherents = Adherent.objects.all()
    context = {'adherents': adherents}
    return render (request , 'base/home.html', context)

def gestionAdherent (request) :
    adherents = Adherent.objects.all()
    context = {'adherents': adherents}
    return render (request , 'base/gestion_adherent.html', context)

def createAdherent(request) : 
    form = AdherentForm()
    if request.method == 'POST' : 
        form=AdherentForm(request.POST)
        if form.is_valid() :
           form.save
           return redirect('home')
    context={'form':form}
    return render(request , 'base/adherent_form.html', context)
