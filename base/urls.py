from django.urls import path
from . import views


urlpatterns = [
   path('', views.home , name="home"),
   path('create-adherent/' , views.createAdherent , name="create-adherent"),
   path('gestion_adherent/' , views.gestionAdherent , name="gestion_adherent"),
   path('update-adherent/<str:pk>/ ', views.updateAdherent , name="update-adherent"),
   path('delete-adherent/<str:pk>/ ', views.deleteAdherent , name="delete-adherent"),
   ]
