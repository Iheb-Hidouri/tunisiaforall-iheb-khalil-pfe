from django.contrib import admin 

# Register your models here.
from .models import BanqueTransactions


admin.site.register(BanqueTransactions)