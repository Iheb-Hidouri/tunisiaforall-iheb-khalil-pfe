from django.db.models.signals import post_save, pre_delete , post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Adherent , AdherentHistory , Structure , StructureHistory , BanqueTransactions , BanqueTransactionHistory , CaisseTransactionHistory, CaisseTransactions
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user



@receiver(post_delete, sender=Adherent)
def post_delete_adherent(sender, instance,request=None , **kwargs,):
    if request is None:
        return
    history = AdherentHistory(user=instance.user.username, adherent=str(instance), action='supprimé')
    history.save()


@receiver(post_save, sender=Adherent)
def post_save_adherent(sender, instance, created,request=None , **kwargs ):
    if request is None:
        return
    action = 'crée' if created else 'mis à jour'
    changes = instance._changes if not created else None
    history = AdherentHistory(user=request.user.username, adherent=str(instance), action=action, changes=changes)
    history.save()

@receiver(post_delete, sender=Structure)
def post_delete_structure(sender, instance,request=None , **kwargs,):
    if request is None:
        return
    history = StructureHistory(user=request.user.username, structure=str(instance), action='supprimé')
    history.save()


@receiver(post_save, sender=Structure)
def post_save_structure(sender, instance, created,request=None , **kwargs ):
    if request is None:
        return
    action = 'crée' if created else 'mis à jour '
    changes = instance._changes if not created else None
    history = StructureHistory(user=request.user.username, structure=str(instance), action=action, changes=changes)
    history.save()

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

      
        
    CaisseTransactionHistory.objects.create(caisse_transaction=caisse_transaction.libellé, action=action, old_data=old_data, new_data=new_data, user=request.user.username)

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
    
    CaisseTransactionHistory.objects.create( caisse_transaction=caisse_transaction.libellé, action=action, old_data=old_data, new_data=new_data , user=request.user.username) 
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

      
        
    BanqueTransactionHistory.objects.create(banque_transaction=banque_transaction.libellé, action=action, old_data=old_data, new_data=new_data, user=request.user.username)

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
    
    BanqueTransactionHistory.objects.create( banque_transaction=banque_transaction.libellé, action=action, old_data=old_data, new_data=new_data , user=request.user.username)
