from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Animal, Habitat

def get_habitats(request):
    habitats = Habitat.objects.all()

    data = []
    for habitat in habitats:
        animals = habitat.animal_set.all()
        data.append({
            'id': habitat.id,
            'name': habitat.name, 
            'size': habitat.size,
            'climate': habitat.climate,
            'animals': [f'{animal.species}, ' for animal in animals]})
    return JsonResponse(data, safe=False)

def add_habitat(request):
    name = request.GET.get('name', '').strip()
    size = request.GET.get('size', '').strip()
    climate = request.GET.get('climate', '').strip()
    
    if not name:
        return JsonResponse({"error": "Habitat name is required."}, status=400)
    if not size:
        return JsonResponse({"error": "Habitat size is required."}, status=400)
    if not climate:
        return JsonResponse({"error": "Habitat climate is required."}, status=400)
    
    try:
        habitat, created = Habitat.objects.get_or_create(
            name=name, 
            defaults={"size": size, "climate": climate}
        )
        
        if not created:
            return JsonResponse({"error": f"Habitat '{name}' already exists."}, status=400)
        
        return JsonResponse({
            "message": "Habitat created successfully!",
            "habitat": {
                "id": habitat.id,
                "name": habitat.name,
                "size": habitat.size,
                "climate": habitat.climate
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def update_habitat(request):
    name = request.GET.get('name', '').strip()
    new_name = request.GET.get('new_name', '').strip()
    size = request.GET.get('size', '').strip()
    climate = request.GET.get('climate', '').strip()
    
    if not name:
        return JsonResponse({"error": "Current habitat name is required to identify the habitat."}, status=400)
    
    try:
        habitat = get_object_or_404(Habitat, name=name)
        
        if new_name:
            if Habitat.objects.filter(name=new_name).exists() and new_name != name:
                return JsonResponse({"error": f"Habitat with name '{new_name}' already exists."}, status=400)
            habitat.name = new_name
        if size:
            habitat.size = size
        if climate:
            habitat.climate = climate
            
        habitat.save()
        
        return JsonResponse({
            "message": f"Habitat '{name}' updated successfully!",
            "updated_habitat": {
                "id": habitat.id,
                "name": habitat.name,
                "size": habitat.size,
                "climate": habitat.climate
            }
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def delete_habitat(request):
    name = request.GET.get('name', '').strip()
    
    if not name:
        return JsonResponse({"error": "Habitat name is required to delete the habitat."}, status=400)
    
    try:
        habitat = get_object_or_404(Habitat, name=name)
        

        if habitat.animal_set.exists():
            return JsonResponse({
                "error": "Cannot delete habitat as it is associated with one or more animals. Remove the animals first."
            }, status=400)
            
        habitat.delete()
        return JsonResponse({"message": f"Habitat '{name}' deleted successfully!"}, status=200)
    except Habitat.DoesNotExist:
        return JsonResponse({"error": f"No habitat found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_habitat_detail(request, name):
    try:
        habitat = get_object_or_404(Habitat, name=name)
        animals = [
            {
                "id": animal.id,
                "species": animal.species
            }
            for animal in habitat.animal_set.all()
        ]
        
        data = {
            "id": habitat.id,
            "name": habitat.name,
            "size": habitat.size,
            "climate": habitat.climate,
            "animals": animals
        }
        return JsonResponse(data)
    except Habitat.DoesNotExist:
        return JsonResponse({"error": f"No habitat found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


def get_animals(request):
    animals = Animal.objects.all()
    data = [
        {
            "id": animal.id,
            "species": animal.species,
            "diet": animal.diet,
            "lifespan": animal.lifespan,
            "behaviour": animal.behaviour,
            "habitats": [habitat.name for habitat in animal.habitat.all()]
        }
        for animal in animals
    ]
    return JsonResponse(data, safe=False)

def add_animal(request):
    species = request.GET.get('species', '').strip()
    diet = request.GET.get('diet', '').strip()
    lifespan = request.GET.get('lifespan', '').strip()
    behaviour = request.GET.get('behaviour', '').strip()
    habitats = request.GET.get('habitats', '').strip()
    
    if not species:
        return JsonResponse({"error": "Animal species is required."}, status=400)
    if not diet:
        return JsonResponse({"error": "Animal diet is required."}, status=400)
    if not lifespan:
        return JsonResponse({"error": "Animal lifespan is required."}, status=400)
    if not behaviour:
        return JsonResponse({"error": "Animal behaviour is required."}, status=400)
    
    try:
        lifespan_value = int(lifespan)
        if lifespan_value <= 0:
            return JsonResponse({"error": "Lifespan must be a positive integer."}, status=400)
    except ValueError:
        return JsonResponse({"error": "Lifespan must be a valid integer."}, status=400)
    
    if Animal.objects.filter(species=species).exists():
        return JsonResponse({"error": f"Animal with species '{species}' already exists."}, status=400)
    
    animal = Animal.create(
        species=species,
        diet=diet,
        lifespan=lifespan_value,
        behaviour=behaviour
    )
    
    if habitats:
        habitat_names = [h.strip() for h in habitats.split(',')]
        found_habitats = Habitat.objects.filter(name__in=habitat_names)
        
        if len(found_habitats) != len(habitat_names):
            missing = set(habitat_names) - set(h.name for h in found_habitats)
            animal.delete()  
            return JsonResponse({
                "error": f"Some habitats were not found: {', '.join(missing)}"
            }, status=404)
        
        animal.habitat.set(found_habitats)
    
    return JsonResponse({
        "message": "Animal created successfully!",
        "animal": {
            "id": animal.id,
            "species": animal.species,
            "diet": animal.diet,
            "lifespan": animal.lifespan,
            "behaviour": animal.behaviour,
            "habitats": [habitat.name for habitat in animal.habitat.all()]
        }
    }, status=201)

def update_animal(request):
    species = request.GET.get('species', '').strip()
    new_species = request.GET.get('new_species', '').strip()
    diet = request.GET.get('diet', '').strip()
    lifespan = request.GET.get('lifespan', '').strip()
    behaviour = request.GET.get('behaviour', '').strip()
    habitats = request.GET.get('habitats', '').strip()
    
    if not species:
        return JsonResponse({"error": "Current animal species is required to identify the animal."}, status=400)
    
    try:
        animal = get_object_or_404(Animal, species=species)
        
        if new_species:
            if Animal.objects.filter(species=new_species).exists() and new_species != species:
                return JsonResponse({"error": f"Animal with species '{new_species}' already exists."}, status=400)
            animal.species = new_species
        
        if diet:
            animal.diet = diet
            
        if lifespan:
            try:
                lifespan_value = int(lifespan)
                if lifespan_value <= 0:
                    return JsonResponse({"error": "Lifespan must be a positive integer."}, status=400)
                animal.lifespan = lifespan_value
            except ValueError:
                return JsonResponse({"error": "Lifespan must be a valid integer."}, status=400)
                
        if behaviour:
            animal.behaviour = behaviour
            
        animal.save()
        
        if habitats:
            habitat_names = [h.strip() for h in habitats.split(',')]
            found_habitats = Habitat.objects.filter(name__in=habitat_names)
            
            if len(found_habitats) != len(habitat_names):
                missing = set(habitat_names) - set(h.name for h in found_habitats)
                return JsonResponse({
                    "error": f"Some habitats were not found: {', '.join(missing)}"
                }, status=404)
            
            animal.habitat.set(found_habitats)
        
        return JsonResponse({
            "message": f"Animal '{species}' updated successfully!",
            "updated_animal": {
                "id": animal.id,
                "species": animal.species,
                "diet": animal.diet,
                "lifespan": animal.lifespan,
                "behaviour": animal.behaviour,
                "habitats": [habitat.name for habitat in animal.habitat.all()]
            }
        }, status=200)
    except Animal.DoesNotExist:
        return JsonResponse({"error": f"No animal found with the species '{species}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def delete_animal(request):
    species = request.GET.get('species', '').strip()
    
    if not species:
        return JsonResponse({"error": "Animal species is required to delete the animal."}, status=400)
    
    try:
        animal = get_object_or_404(Animal, species=species)
        animal.delete()
        return JsonResponse({"message": f"Animal '{species}' deleted successfully!"}, status=200)
    except Animal.DoesNotExist:
        return JsonResponse({"error": f"No animal found with the species '{species}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_animal_detail(request, species):
    try:
        animal = get_object_or_404(Animal, species=species)
        habitats = [
            {
                "id": habitat.id,
                "name": habitat.name
            }
            for habitat in animal.habitat.all()
        ]
        
        data = {
            "id": animal.id,
            "species": animal.species,
            "diet": animal.diet,
            "lifespan": animal.lifespan,
            "behaviour": animal.behaviour,
            "habitats": habitats
        }
        return JsonResponse(data)
    except Animal.DoesNotExist:
        return JsonResponse({"error": f"No animal found with the species '{species}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
