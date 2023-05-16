from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Adherent , AdherentHistory , Structure , StructureHistory , BanqueTransactions , BanqueTransactionHistory , CaisseTransactionHistory, CaisseTransactions
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model




@receiver(post_save, sender=Adherent)
def save_adherent_history(sender, instance, created,request=None , **kwargs):
    if request is None:
        return
    adherent = instance
    if created:
        action = 'Created'
        old_data = ''
        new_data = f'{instance}'
    else:
        action = 'Updated'
        old_data = f'{instance}'
        new_data = f'{instance}'

      
        
    AdherentHistory.objects.create(adherent=adherent.nom, action=action, old_data=old_data, new_data=new_data, user=request.user.username)

@receiver(pre_delete, sender=Adherent)
def delete_adherent_history(sender, instance,request=None, **kwargs):
    print("delete_adherent_history signal triggered!")
    
    if request is None:
        print("No request object found!")
        return
    adherent = instance
    action = 'Deleted'
    old_data = f'{instance}'
    new_data = ''
    
    AdherentHistory.objects.create( adherent=adherent.nom, action=action, old_data=old_data, new_data=new_data , user=request.user.username)

@receiver(post_save, sender=Structure)
def save_structure_history(sender, instance, created,request=None , **kwargs):
    if request is None:
        return
    structure = instance
    if created:
        action = 'Created'
        old_data = ''
        new_data = f'{instance}'
    else:
        action = 'Updated'
        old_data = f'{instance}'
        new_data = f'{instance}'

      
        
    StructureHistory.objects.create(structure=structure.libelle, action=action, old_data=old_data, new_data=new_data, user=request.user.username)

@receiver(pre_delete, sender=Structure)
def delete_structure_history(sender, instance,request=None, **kwargs):
    print("delete_adherent_history signal triggered!")
    
    if request is None:
        print("No request object found!")
        return
    structure = instance
    action = 'Deleted'
    old_data = f'{instance}'
    new_data = ''
    
    StructureHistory.objects.create( structure=structure.libelle, action=action, old_data=old_data, new_data=new_data , user=request.user.username)    

@receiver(post_save, sender=CaisseTransactions)
def save_caisse_transaction_history(sender, instance, created,request=None , **kwargs):
    if request is None:
        return
    caisse_transaction = instance
    if created:
        action = 'Created'
        old_data = ''
        new_data = f'{instance}'
    else:
        action = 'Updated'
        old_data = f'{instance}'
        new_data = f'{instance}'

      
        
    CaisseTransactionHistory.objects.create(caisse_transaction=caisse_transaction.libelle, action=action, old_data=old_data, new_data=new_data, user=request.user.username)

@receiver(pre_delete, sender=CaisseTransactions)
def delete_caisse_transaction_history(sender, instance,request=None, **kwargs):
    print("delete_adherent_history signal triggered!")
    
    if request is None:
        print("No request object found!")
        return
    caisse_transaction = instance
    action = 'Deleted'
    old_data = f'{instance}'
    new_data = ''
    
    CaisseTransactionHistory.objects.create( caisse_transaction=caisse_transaction.libelle, action=action, old_data=old_data, new_data=new_data , user=request.user.username) 
@receiver(post_save, sender=BanqueTransactions)
def save_banque_transaction_history(sender, instance, created,request=None , **kwargs):
    if request is None:
        return
    banque_transaction = instance
    if created:
        action = 'Created'
        old_data = ''
        new_data = f'{instance}'
    else:
        action = 'Updated'
        old_data = f'{instance}'
        new_data = f'{instance}'

      
        
    BanqueTransactionHistory.objects.create(banque_transaction=banque_transaction.libelle, action=action, old_data=old_data, new_data=new_data, user=request.user.username)

@receiver(pre_delete, sender=BanqueTransactions)
def delete_banque_transaction_history(sender, instance,request=None, **kwargs):
    print("delete_adherent_history signal triggered!")
    
    if request is None:
        print("No request object found!")
        return
    banque_transaction = instance
    action = 'Deleted'
    old_data = f'{instance}'
    new_data = ''
    
    BanqueTransactionHistory.objects.create( banque_transaction=banque_transaction.libelle, action=action, old_data=old_data, new_data=new_data , user=request.user.username)
