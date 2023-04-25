from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Adherent , AdherentHistory
from django.contrib.auth.models import User 


@receiver(post_save, sender=Adherent)
def save_adherent_history( instance, created, **kwargs):
    
    adherent = instance
    if created:
        action = 'Created'
        old_data = ''
        new_data = f'{instance}'
    else:
        action = 'Updated'
        old_data = f'{instance}'
        new_data = f'{instance}'
    AdherentHistory.objects.create(adherent=adherent, action=action, old_data=old_data, new_data=new_data)

@receiver( pre_delete, sender=Adherent)
def delete_adherent_history(sender, instance, **kwargs):
    
    adherent = instance
    action = 'Deleted'
    old_data = f'{instance}'
    new_data = ''
    AdherentHistory.objects.create( adherent=adherent, action=action, old_data=old_data, new_data=new_data)


