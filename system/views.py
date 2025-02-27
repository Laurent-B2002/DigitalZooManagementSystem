from django.shortcuts import render
from .models import Animal, Habitat
from django.http import JsonResponse
import json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
def all_animals(request):
    animals = Animal.objects.all()
    result = []
    for animal in animals:
        result.append({
            'id': animal.id,
            'name': animal.name,
            'habitat': animal.habitat.name if animal.habitat else None
        })
    return JsonResponse(result, safe=False)

def all_habitats(request):
    habitats = Habitat.objects.all()
    result = []
    for habitat in habitats:
        result.append({
            'id': habitat.id,
            'name': habitat.name, 
            'animals': [f'{animal.name}, ' for animal in habitat.animals.all()]})
    return JsonResponse(result, safe=False)

@csrf_exempt 
def add_animal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            habitat_id = data.get('hid')

            habitat = Habitat.objects.get(id=habitat_id)
            with transaction.atomic():
                new_animal = Animal.objects.create(name=name, habitat=habitat)

            return JsonResponse({
                'id': new_animal.id,
                'name': new_animal.name,
                'habitat': new_animal.habitat.name
            }, status=201)
        except Habitat.DoesNotExist:
            return JsonResponse({'error': 'Habitat not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def add_habitat(request):
    try:
        name = request.GET.get('name')
        with transaction.atomic():
            new_habitat = Habitat.objects.create(name = name)
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'New habitat added: ID = {new_habitat.id}, Name = {new_habitat.name}', safe=False)

@csrf_exempt
def delete_animal(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            animal_id = data.get('aid')

            with transaction.atomic():
                animal = Animal.objects.get(id=animal_id)
                animal.delete()

            return JsonResponse({'message': f'Animal with ID {animal_id} deleted'}, status=200)
        except Animal.DoesNotExist:
            return JsonResponse({'error': 'Animal not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_habitat(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            habitat_id = data.get('hid')

            with transaction.atomic():
                habitat = Habitat.objects.get(id=habitat_id)
                habitat.delete()

            return JsonResponse({'message': f'Habitat with ID {habitat_id} deleted'}, status=200)
        except Habitat.DoesNotExist:
            return JsonResponse({'error': 'Animal not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def update_animal(request):
    try:
        animal_id = request.GET.get('aid')
        animal_name = request.GET.get('name')
        habitat_id = request.GET.get('hid')
        diet = request.GET.get('diet')
        lifespan = request.GET.get('lifespan')
        behavior = request.GET.get('behavior')
        with transaction.atomic():
            animal = Animal.objects.get(id = animal_id)
            if animal_name:
                animal.name = animal_name
            if habitat_id:
                habitat = Habitat.objects.get(id = habitat_id)
                animal.habitat = habitat
            if diet:
                animal.diet = diet
            if lifespan:
                animal.lifespan = lifespan
            if behavior:
                animal.behavior = behavior
            animal.save()
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'Animal with ID {animal_id} updated. Name: {animal.name}, Habitat: {animal.habitat.name}', safe=False)

def update_habitat(request):
    try:
        habitat_name = request.GET.get('name')
        habitat_id = request.GET.get('hid')
        habitat_size = request.GET.get('size')
        habitat_climate = request.GET.get('climate')
        habitat_species = request.GET.get('suitable_species')
        with transaction.atomic():
            habitat = Habitat.objects.get(id = habitat_id)
            if habitat_name:
                habitat.name = habitat_name
            if habitat_size:
                habitat.size = habitat_size
            if habitat_climate:
                habitat.climate = habitat_climate
            if habitat_species:
                habitat.suitable_species = habitat_species
            habitat.save()
    except Exception as e:
        return(f"Something went wrong: {e}")
    return JsonResponse(f'Habitat with ID {habitat.id} updated. Name: {habitat.name}', safe=False)
