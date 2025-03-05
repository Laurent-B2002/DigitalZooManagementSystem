from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('habitats/', views.get_habitats, name='get_habitats'),
    path('habitats/add/', views.add_habitat, name='add_habitat'),
    path('habitats/update/', views.update_habitat, name='update_habitat'),
    path('habitats/delete/', views.delete_habitat, name='delete_habitat'),
    path('habitats/<str:name>/', views.get_habitat_detail, name='get_habitat_detail'),
    path('species/', views.get_species, name='get_species'),
    path('species/add/', views.add_species, name='add_species'),
    path('species/update/', views.update_species, name='update_species'),
    path('species/delete/', views.delete_species, name='delete_species'),
    path('species/<str:name>/', views.get_species_detail, name='get_species_detail'),
    path('animals/', views.get_animals, name='get_animals'),
    path('animals/add/', views.add_animal, name='add_animal'),
    path('animals/update/', views.update_animal, name='update_animal'),
    path('animals/delete/', views.delete_animal, name='delete_animal'),
    path('animals/<str:name>/', views.get_animal_detail, name='get_animal_detail'),
    path('zookeepers/', views.get_zookeepers, name='get_zookeepers'),
    path('zookeepers/add/', views.add_zookeeper, name='add_zookeeper'),
    path('zookeepers/update/', views.update_zookeeper, name='update_zookeeper'),
    path('zookeepers/delete/', views.delete_zookeeper, name='delete_zookeeper'),
    path('zookeepers/<str:name>/', views.get_zookeeper_detail, name='get_zookeeper_detail'),
    path('care-routines/', views.get_care_routines, name='get_care_routines'),
    path('care-routines/add/', views.add_care_routine, name='add_care_routine'),
    path('care-routines/update/', views.update_care_routine, name='update_care_routine'),
    path('care-routines/delete/', views.delete_care_routine, name='delete_care_routine'),
    path('care-routines/<int:routine_id>/', views.get_care_routine_detail, name='get_care_routine_detail'),
]

