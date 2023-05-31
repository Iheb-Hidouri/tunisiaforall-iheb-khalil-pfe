from django.contrib import admin

from .models import  StructureHistory ,Adherent , Structure , Governat , Delegation , AdherentHistory , BanqueTransactions , CaisseTransactions , BanqueTransactionHistory , CaisseTransactionHistory, Cotisation, Evenement

admin.site.register(Adherent)
admin.site.register(Structure)
admin.site.register(Governat)
admin.site.register(Delegation)
admin.site.register(AdherentHistory)
admin.site.register(StructureHistory)
admin.site.register(BanqueTransactions)
admin.site.register(CaisseTransactions)
admin.site.register(CaisseTransactionHistory)
admin.site.register(BanqueTransactionHistory)
admin.site.register(Cotisation)
admin.site.register(Evenement)
