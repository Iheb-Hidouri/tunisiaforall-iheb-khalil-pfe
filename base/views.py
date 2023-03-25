from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Adherent
from .forms import AdherentForm




def home (request) : 
   
    return render (request , 'base/home.html')

def gestionAdherent (request) :
    adherents = Adherent.objects.all()
    context = {'adherents': adherents}
    return render (request , 'base/gestion_adherent.html', context)

def createAdherent(request) : 
    form = AdherentForm()
    if request.method == 'POST' : 
        form=AdherentForm(request.POST)
        if form.is_valid() :
           form.save()
           return redirect('home')
    context={'form':form}
    return render(request , 'base/adherent_form.html', context)

def updateAdherent(request , pk) : 
    adherent = Adherent.objects.get(id=pk)
    form = AdherentForm(instance=adherent)
    if request.method == 'POST' :
        form=AdherentForm(request.POST , instance=adherent)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form' : form}
    return render(request , 'base/adherent_form.html', context)


def deleteAdherent(request , pk) :
    adherent= Adherent.objects.get(id=pk)
    if request.method =='POST' : 
        adherent.delete()
        return redirect('gestion_adherent')
    return render (request , 'base/delete.html', {'obj': adherent})