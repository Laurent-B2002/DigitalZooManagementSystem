from django.urls import path
from . import views

urlpatterns = [
    path('habitats/', views.get_habitats, name='get_habitats'),
    path('habitats/add/', views.add_habitat, name='add_habitat'),
    path('habitats/update/', views.update_habitat, name='update_habitat'),
    path('habitats/delete/', views.delete_habitat, name='delete_habitat'),
    path('habitats/<str:name>/', views.get_habitat_detail, name='get_habitat_detail'),
    path('animals/', views.get_animals, name='get_animals'),
    path('animals/add/', views.add_animal, name='add_animal'),
    path('animals/update/', views.update_animal, name='update_animal'),
    path('animals/delete/', views.delete_animal, name='delete_animal'),
    path('animals/<str:species>/', views.get_animal_detail, name='get_animal_detail'),
]

