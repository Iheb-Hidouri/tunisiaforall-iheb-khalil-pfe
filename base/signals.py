from django.db.models.signals import post_save, pre_delete , post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import TransactionHistory ,Adherent , AdherentHistory , Structure , StructureHistory , BanqueTransactions , BanqueTransactionHistory , CaisseTransactionHistory, CaisseTransactions
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user



@receiver(post_delete, sender=Adherent)
def post_delete_adherent(sender, instance,request=None , **kwargs,):
    if request is None:
        return
    history = AdherentHistory(user =request.user.username, adherent=str(instance), action='supprimé')
    history.save()


@receiver(post_save, sender=Adherent)
def post_save_adherent(sender, instance, created,request=None , **kwargs ):
    if request is None:
        return
    action = 'crée' if created else 'mis à jour'
    changes = instance._changes if not created else None
    history = AdherentHistory(user =request.user.username, adherent=str(instance), action=action, changes=changes)
    history.save()
@receiver(post_delete, sender=BanqueTransactions)
def post_delete_banquetransaction(sender, instance,request=None , **kwargs,):
    if request is None:
        return
    history = TransactionHistory(user =request.user.username, transaction=str(instance), action='supprimé')
    history.save()


@receiver(post_save, sender=BanqueTransactions)
def post_save_banquetransaction(sender, instance, created,request=None , **kwargs ):
    if request is None:
        return
    action = 'crée' if created else 'mis à jour'
    changes = instance._changes if not created else None
    history = TransactionHistory(user =request.user.username, transaction=str(instance), action=action, changes=changes)
    history.save()   

@receiver(post_delete, sender=CaisseTransactions)
def post_delete_caissetransaction(sender, instance,request=None , **kwargs,):
    if request is None:
        return
    history = TransactionHistory(user =request.user.username, transaction=str(instance), action='supprimé')
    history.save()


@receiver(post_save, sender=CaisseTransactions)
def post_save_caissetransaction(sender, instance, created,request=None , **kwargs ):
    if request is None:
        return
    action = 'crée' if created else 'mis à jour'
    changes = instance._changes if not created else None
    history = TransactionHistory(user =request.user.username, transaction=str(instance), action=action, changes=changes)
    history.save()         

@receiver(post_delete, sender=Structure)
def post_delete_structure(sender, instance,request=None , **kwargs,):
    if request is None:
        return
    history = StructureHistory(user =request.user.username, structure=str(instance), action='supprimé')
    history.save()


@receiver(post_save, sender=Structure)
def post_save_structure(sender, instance, created,request=None , **kwargs ):
    if request is None:
        return
    action = 'crée' if created else 'mis à jour '
    changes = instance._changes if not created else None
    history = StructureHistory(user =request.user.username, structure=str(instance), action=action, changes=changes)
    history.save()


