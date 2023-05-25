from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
   path('gestion_financiere/' , views.gestion_financiere , name="gestion_financiere"),
   path('create-banque-transaction/' , views.create_banque_transaction , name="create-banque-transaction"),
   path('update-banque-transaction/<str:pk>/ ' , views.update_banque_transaction , name="update-banque-transaction"),
   path('create-caisse-transaction/' , views.create_caisse_transaction , name="create-caisse-transaction"),
   path('update-caisse-transaction/<str:pk>/ ' , views.update_caisse_transaction , name="update-caisse-transaction"),
  
  ]