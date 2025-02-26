from . import views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('animals/', views.all_animals, name='sample_json_view'),
    path('habitats/', views.all_habitats, name='sample_json_view'),
    path('add_animal/', views.add_animal, name='sample_json_view'),
    path('add_habitat/', views.add_habitat, name='sample_json_view'),
    path('delete_animal/', views.delete_animal, name='sample_json_view'),
    path('delete_habitat/', views.delete_habitat, name='sample_json_view'),
    path('update_animal/', views.update_animal, name='sample_json_view'),
    path('update_habitat/', views.update_habitat, name='sample_json_view'),
]