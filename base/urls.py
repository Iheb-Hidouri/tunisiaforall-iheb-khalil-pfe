from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import adherent_history



urlpatterns = [
   path('login/' , views.loginPage , name="login") ,
   path('logout/' , views.logoutUser, name="logout") ,
   path('', views.home , name="home"),
   path('create-adherent/' , views.create_adherent , name="create-adherent"),
   path('gestion_adherent/' , views.gestion_adherent , name="gestion_adherent"),
   path('gestion_structure/' , views.gestion_structure , name="gestion_structure"),
   path('update-adherent/<str:pk>/ ', views.update_adherent , name="update-adherent"),
   path('delete-adherent/<str:pk>/ ', views.delete_adherent , name="delete-adherent"),
   path('create-structure/' , views.create_structure , name="create-structure"),
   path('update-structure/<str:pk>/', views.update_structure, name="update-structure"),
   path('delete-structure/<str:pk>/', views.delete_structure , name="delete-structure"),
   path('adherent_history/', views.adherent_history, name='adherent_history'),
   path('structure_history/', views.structure_history, name='structure_history'),
   path('gestion_financiere/' , views.gestion_financiere , name="gestion_financiere"),
   path('create-banque-transaction/' , views.create_banque_transaction , name="create-banque-transaction"),
   path('update-banque-transaction/<str:pk>/ ' , views.update_banque_transaction , name="update-banque-transaction"),
   path('create-caisse-transaction/' , views.create_caisse_transaction , name="create-caisse-transaction"),
   path('update-caisse-transaction/<str:pk>/ ' , views.update_caisse_transaction , name="update-caisse-transaction"),
   path('delete-banque-transaction/<int:pk>/', views.delete_banque_transaction, name='delete-banque-transaction'),
   path('delete-caisse-transaction/<int:pk>/', views.delete_caisse_transaction, name='delete-caisse-transaction'),
   path('payer_ma_cotisation/', views.payer_ma_cotisation, name='payer_ma_cotisation'),
   path('profile/', views.profile, name='profile'),
   path('fetch-delegations/', views.fetch_delegations, name='fetch_delegations'),
   path('consult_adherent/<str:pk>/', views.consult_adherent, name='consult_adherent'),
   path('consult_structure/<str:pk>/', views.consult_structure, name='consult_structure'),
   path('consult_banque_transaction/<str:pk>/', views.consult_banque_transaction, name='consult_banque_transaction'),
   path('consult_caisse_transaction/<str:pk>/', views.consult_caisse_transaction, name='consult_caisse_transaction'),
   
  
  ]

