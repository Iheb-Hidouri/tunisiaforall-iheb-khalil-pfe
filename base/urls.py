from django.urls import path
from . import views


urlpatterns = [
   path('', views.home , name="home"),
   path('create-adherent/' , views.createAdherent , name="create-adherent"),
   path('gestion_adherent/' , views.gestionAdherent , name="gestion_adherent")
]
