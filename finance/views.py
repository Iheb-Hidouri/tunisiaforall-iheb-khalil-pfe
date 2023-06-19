from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BanqueTransactionsForm, CaisseTransactionsForm
from .models import BanqueTransactions, CaisseTransactions

def gestion_financiere(request):
    # Get the search query from the GET request parameters
   
        # If no search query is present, display all adherents
    banque_transactions = BanqueTransactions.objects.all() 
    caisse_transactions = CaisseTransactions.objects.all()

    # Combine the instances into a single list
    transactions = list(banque_transactions) + list(caisse_transactions)

    # Pass the transactions to the template
    context = {'transactions': transactions }
    # Create a dictionary with the adherents queryset and pass it to the template
    
    return render(request, 'finance/gestion_financiere.html', context)

def create_banque_transaction(request):
    if request.method == 'POST':
        form = BanqueTransactionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your desired URL
    else:
        form = BanqueTransactionsForm()
    return render(request, 'finance/banque_form.html', {'form': form})

def update_banque_transaction(request, pk):
    transaction = get_object_or_404(BanqueTransactions, id=pk)
    if request.method == 'POST':
        form = BanqueTransactionsForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your desired URL
    else:
        form = BanqueTransactionsForm(instance=transaction)
    return render(request, 'finance/banque_form.html', {'form': form})

# Similar functions for CaisseTransactions
def create_caisse_transaction(request):
    if request.method == 'POST':
        form = CaisseTransactionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your desired URL
    else:
        form = CaisseTransactionsForm()
    return render(request, 'finance/caisse_form.html', {'form': form})

def update_caisse_transaction(request, pk):
    transaction = get_object_or_404(CaisseTransactions, id=pk)
    if request.method == 'POST':
        form = CaisseTransactionsForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your desired URL
    else:
        form = CaisseTransactionsForm(instance=transaction)
    return render(request, 'finance/caisse_form.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import get_object_or_404, redirect







