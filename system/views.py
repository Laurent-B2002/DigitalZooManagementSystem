from django.shortcuts import render
from .models import Animal, Habitat
from django.http import JsonResponse
from django.db import transaction
def all_animals(request):
    animals = Animal.objects.all()
    result = []
    for animal in animals:
        result.append(f'Animal: {animal.name}, Habitat: {animal.habitat.name}')
    return JsonResponse(result, safe=False)

def all_habitats(request):
    habitats = Habitat.objects.all()
    result = {}
    for habitat in habitats:
        result[habitat.name] = [animal.name for animal in habitat.animals.all()]
    return JsonResponse(result, safe=False)

def add_animal(request):
    try:
        name = request.GET.get('name')
        habitat_id = request.GET.get('hid')
        habitat = Habitat.objects.get(id=habitat_id)
        with transaction.atomic():
            new_animal = Animal.objects.create(name = name, habitat = habitat)
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'New animal added: ID = {new_animal.id}, Name = {new_animal.name}, Habitat = {new_animal.habitat.name}', safe=False)

def add_habitat(request):
    try:
        name = request.GET.get('name')
        with transaction.atomic():
            new_habitat = Habitat.objects.create(name = name)
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'New habitat added: ID = {new_habitat.id}, Name = {new_habitat.name}', safe=False)

def delete_animal(request):
    try:
        animal_id = request.GET.get('aid')
        with transaction.atomic():
            animal = Animal.objects.get(id = animal_id)
            animal.delete()
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'Animal with ID {animal_id} deleted', safe=False)

def delete_habitat(request):
    try:
        habitat_id = request.GET.get('hid')
        with transaction.atomic():
            habitat = Habitat.objects.get(id = habitat_id)
            habitat.delete()
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'Animal with ID {habitat_id} deleted', safe=False)

def update_animal(request):
    try:
        animal_id = request.GET.get('aid')
        animal_name = request.GET.get('name')
        habitat_id = request.GET.get('hid')
        with transaction.atomic():
            animal = Animal.objects.get(id = animal_id)
            if animal_name:
                animal.name = animal_name
            if habitat_id:
                habitat = Habitat.objects.get(id = habitat_id)
                animal.habitat = habitat
            animal.save()
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'Animal with ID {animal_id} updated. Name: {animal.name}, Habitat: {animal.habitat.name}', safe=False)

def update_habitat(request):
    try:
        habitat_name = request.GET.get('name')
        habitat_id = request.GET.get('hid')
        with transaction.atomic():
            habitat = Habitat.objects.get(id = habitat_id)
            if habitat_name:
                habitat.name = habitat_name
            habitat.save()
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'Habitat with ID {habitat.id} updated. Name: {habitat.name}', safe=False)
