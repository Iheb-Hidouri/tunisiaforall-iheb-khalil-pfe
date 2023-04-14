from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
   path('', views.home , name="home"),
   path('create-adherent/' , views.create_adherent , name="create-adherent"),
   path('gestion_adherent/' , views.gestion_adherent , name="gestion_adherent"),
   path('gestion_structure/' , views.gestion_structure , name="gestion_structure"),
   path('update-adherent/<str:pk>/ ', views.update_adherent , name="update-adherent"),
   path('delete-adherent/<str:pk>/ ', views.delete_adherent , name="delete-adherent"),
   path('create-structure/' , views.create_structure , name="create-structure"),
   path('update-structure/<str:pk>/', views.update_structure, name="update-structure"),
   path('delete-structure/<str:pk>/', views.delete_structure , name="delete-structure"),
  ]

