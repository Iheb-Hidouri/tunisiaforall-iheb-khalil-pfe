from django.contrib import admin

from .models import Adherent , Structure , Governat , Delegation , AdherentHistory , BanqueTransactions , CaisseTransactions , BanqueTransactionHistory , CaisseTransactionHistory, Cotisation

admin.site.register(Adherent)
admin.site.register(Structure)
admin.site.register(Governat)
admin.site.register(Delegation)
admin.site.register(AdherentHistory)
admin.site.register(BanqueTransactions)
admin.site.register(CaisseTransactions)
admin.site.register(CaisseTransactionHistory)
admin.site.register(BanqueTransactionHistory)
admin.site.register(Cotisation)