from django import template
from base.models import BanqueTransactions , CaisseTransactions

register = template.Library()

@register.filter
def is_banque_transaction(transaction):
    return isinstance(transaction, BanqueTransactions)

def is_caisse_transaction(transaction):
    return isinstance(transaction, CaisseTransactions)
