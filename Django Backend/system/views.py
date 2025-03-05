from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Animal, Habitat, Species, Zookeeper, CareRoutine

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
            'animals': [animal.name for animal in animals]
        })
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
                "name": animal.name,
                "species": animal.species.name
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

def get_species(request):
    species_list = Species.objects.all()
    data = [
        {
            "id": species.id,
            "name": species.name,
            "animal_count": species.animals.count()
        }
        for species in species_list
    ]
    return JsonResponse(data, safe=False)

def add_species(request):
    name = request.GET.get('name', '').strip()
    
    if not name:
        return JsonResponse({"error": "Species name is required."}, status=400)
    
    try:
        species, created = Species.objects.get_or_create(name=name)
        
        if not created:
            return JsonResponse({"error": f"Species '{name}' already exists."}, status=400)
        
        return JsonResponse({
            "message": "Species created successfully!",
            "species": {
                "id": species.id,
                "name": species.name
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def update_species(request):
    name = request.GET.get('name', '').strip()
    new_name = request.GET.get('new_name', '').strip()
    
    if not name:
        return JsonResponse({"error": "Current species name is required to identify the species."}, status=400)
    if not new_name:
        return JsonResponse({"error": "New species name is required for update."}, status=400)
    
    try:
        species = get_object_or_404(Species, name=name)
        
        if Species.objects.filter(name=new_name).exists() and new_name != name:
            return JsonResponse({"error": f"Species with name '{new_name}' already exists."}, status=400)
        
        species.name = new_name
        species.save()
        
        return JsonResponse({
            "message": f"Species '{name}' updated successfully!",
            "updated_species": {
                "id": species.id,
                "name": species.name
            }
        }, status=200)
    except Species.DoesNotExist:
        return JsonResponse({"error": f"No species found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def delete_species(request):
    name = request.GET.get('name', '').strip()
    
    if not name:
        return JsonResponse({"error": "Species name is required to delete the species."}, status=400)
    
    try:
        species = get_object_or_404(Species, name=name)
        
        if species.animals.exists():
            return JsonResponse({
                "error": "Cannot delete species as it is associated with one or more animals. Remove the animals first."
            }, status=400)
            
        species.delete()
        return JsonResponse({"message": f"Species '{name}' deleted successfully!"}, status=200)
    except Species.DoesNotExist:
        return JsonResponse({"error": f"No species found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_species_detail(request, name):
    try:
        species = get_object_or_404(Species, name=name)
        animals = [
            {
                "id": animal.id,
                "name": animal.name
            }
            for animal in species.animals.all()
        ]
        
        data = {
            "id": species.id,
            "name": species.name,
            "animals": animals
        }
        return JsonResponse(data)
    except Species.DoesNotExist:
        return JsonResponse({"error": f"No species found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_animals(request):
    animals = Animal.objects.all()
    data = [
        {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species.name,
            "diet": animal.diet,
            "lifespan": animal.lifespan,
            "behaviour": animal.behaviour,
            "habitats": [habitat.name for habitat in animal.habitat.all()]
        }
        for animal in animals
    ]
    return JsonResponse(data, safe=False)

def add_animal(request):
    name = request.GET.get('name', '').strip()
    species_name = request.GET.get('species', '').strip()
    diet = request.GET.get('diet', '').strip()
    lifespan = request.GET.get('lifespan', '').strip()
    behaviour = request.GET.get('behaviour', '').strip()
    habitats = request.GET.get('habitats', '').strip()
    
    if not name:
        return JsonResponse({"error": "Animal name is required."}, status=400)
    if not species_name:
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
    
    if Animal.objects.filter(name=name).exists():
        return JsonResponse({"error": f"Animal with name '{name}' already exists."}, status=400)
    
    try:
        species, _ = Species.objects.get_or_create(name=species_name)
    except Exception as e:
        return JsonResponse({"error": f"Error with species: {str(e)}"}, status=400)
        
    animal = Animal.create(
        name=name,
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
            "name": animal.name,
            "species": animal.species.name,
            "diet": animal.diet,
            "lifespan": animal.lifespan,
            "behaviour": animal.behaviour,
            "habitats": [habitat.name for habitat in animal.habitat.all()]
        }
    }, status=201)

def update_animal(request):
    name = request.GET.get('name', '').strip()
    new_name = request.GET.get('new_name', '').strip()
    species_name = request.GET.get('species', '').strip()
    diet = request.GET.get('diet', '').strip()
    lifespan = request.GET.get('lifespan', '').strip()
    behaviour = request.GET.get('behaviour', '').strip()
    habitats = request.GET.get('habitats', '').strip()
    
    if not name:
        return JsonResponse({"error": "Current animal name is required to identify the animal."}, status=400)
    
    try:
        animal = get_object_or_404(Animal, name=name)
        
        if new_name:
            if Animal.objects.filter(name=new_name).exists() and new_name != name:
                return JsonResponse({"error": f"Animal with name '{new_name}' already exists."}, status=400)
            animal.name = new_name
        
        if species_name:
            try:
                species, _ = Species.objects.get_or_create(name=species_name)
                animal.species = species
            except Exception as e:
                return JsonResponse({"error": f"Error with species: {str(e)}"}, status=400)
        
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
            "message": f"Animal '{name}' updated successfully!",
            "updated_animal": {
                "id": animal.id,
                "name": animal.name,
                "species": animal.species.name,
                "diet": animal.diet,
                "lifespan": animal.lifespan,
                "behaviour": animal.behaviour,
                "habitats": [habitat.name for habitat in animal.habitat.all()]
            }
        }, status=200)
    except Animal.DoesNotExist:
        return JsonResponse({"error": f"No animal found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def delete_animal(request):
    name = request.GET.get('name', '').strip()
    
    if not name:
        return JsonResponse({"error": "Animal name is required to delete the animal."}, status=400)
    
    try:
        animal = get_object_or_404(Animal, name=name)
        animal.delete()
        return JsonResponse({"message": f"Animal '{name}' deleted successfully!"}, status=200)
    except Animal.DoesNotExist:
        return JsonResponse({"error": f"No animal found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_animal_detail(request, name):
    try:
        animal = get_object_or_404(Animal, name=name)
        habitats = [
            {
                "id": habitat.id,
                "name": habitat.name
            }
            for habitat in animal.habitat.all()
        ]
        
        data = {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species.name,
            "diet": animal.diet,
            "lifespan": animal.lifespan,
            "behaviour": animal.behaviour,
            "habitats": habitats
        }
        return JsonResponse(data)
    except Animal.DoesNotExist:
        return JsonResponse({"error": f"No animal found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_zookeepers(request):
    zookeepers = Zookeeper.objects.all()
    data = [
        {
            "id": zookeeper.id,
            "name": zookeeper.name,
            "qualification": zookeeper.qualification,
            "responsibilities": zookeeper.responsibilities,
            "care_routines_count": zookeeper.care_routines.count()
        }
        for zookeeper in zookeepers
    ]
    return JsonResponse(data, safe=False)

def add_zookeeper(request):
    name = request.GET.get('name', '').strip()
    qualification = request.GET.get('qualification', '').strip()
    responsibilities = request.GET.get('responsibilities', '').strip()
    
    if not name:
        return JsonResponse({"error": "Zookeeper name is required."}, status=400)
    if not qualification:
        return JsonResponse({"error": "Zookeeper qualification is required."}, status=400)
    if not responsibilities:
        return JsonResponse({"error": "Zookeeper responsibilities are required."}, status=400)
    
    try:
        zookeeper, created = Zookeeper.objects.get_or_create(
            name=name,
            defaults={
                "qualification": qualification,
                "responsibilities": responsibilities
            }
        )
        
        if not created:
            return JsonResponse({"error": f"Zookeeper '{name}' already exists."}, status=400)
        
        return JsonResponse({
            "message": "Zookeeper created successfully!",
            "zookeeper": {
                "id": zookeeper.id,
                "name": zookeeper.name,
                "qualification": zookeeper.qualification,
                "responsibilities": zookeeper.responsibilities
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def update_zookeeper(request):
    name = request.GET.get('name', '').strip()
    new_name = request.GET.get('new_name', '').strip()
    qualification = request.GET.get('qualification', '').strip()
    responsibilities = request.GET.get('responsibilities', '').strip()
    
    if not name:
        return JsonResponse({"error": "Current zookeeper name is required to identify the zookeeper."}, status=400)
    
    try:
        zookeeper = get_object_or_404(Zookeeper, name=name)
        
        if new_name:
            if Zookeeper.objects.filter(name=new_name).exists() and new_name != name:
                return JsonResponse({"error": f"Zookeeper with name '{new_name}' already exists."}, status=400)
            zookeeper.name = new_name
        if qualification:
            zookeeper.qualification = qualification
        if responsibilities:
            zookeeper.responsibilities = responsibilities
            
        zookeeper.save()
        
        return JsonResponse({
            "message": f"Zookeeper '{name}' updated successfully!",
            "updated_zookeeper": {
                "id": zookeeper.id,
                "name": zookeeper.name,
                "qualification": zookeeper.qualification,
                "responsibilities": zookeeper.responsibilities
            }
        }, status=200)
    except Zookeeper.DoesNotExist:
        return JsonResponse({"error": f"No zookeeper found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def delete_zookeeper(request):
    name = request.GET.get('name', '').strip()
    
    if not name:
        return JsonResponse({"error": "Zookeeper name is required to delete the zookeeper."}, status=400)
    
    try:
        zookeeper = get_object_or_404(Zookeeper, name=name)
        
        if zookeeper.care_routines.exists():
            return JsonResponse({
                "error": "Cannot delete zookeeper as they are assigned to one or more care routines. Remove from care routines first."
            }, status=400)
            
        zookeeper.delete()
        return JsonResponse({"message": f"Zookeeper '{name}' deleted successfully!"}, status=200)
    except Zookeeper.DoesNotExist:
        return JsonResponse({"error": f"No zookeeper found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_zookeeper_detail(request, name):
    try:
        zookeeper = get_object_or_404(Zookeeper, name=name)
        care_routines = [
            {
                "id": routine.id,
                "feeding_time": routine.feeding_time.strftime('%H:%M'),
                "diet": routine.diet
            }
            for routine in zookeeper.care_routines.all()
        ]
        
        data = {
            "id": zookeeper.id,
            "name": zookeeper.name,
            "qualification": zookeeper.qualification,
            "responsibilities": zookeeper.responsibilities,
            "care_routines": care_routines
        }
        return JsonResponse(data)
    except Zookeeper.DoesNotExist:
        return JsonResponse({"error": f"No zookeeper found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_care_routines(request):
    routines = CareRoutine.objects.all()
    data = [
        {
            "id": routine.id,
            "feeding_time": routine.feeding_time.strftime('%H:%M'),
            "diet": routine.diet,
            "medical_needs": routine.medical_needs,
            "zookeepers": [zookeeper.name for zookeeper in routine.zookeepers.all()]
        }
        for routine in routines
    ]
    return JsonResponse(data, safe=False)

def add_care_routine(request):
    feeding_time = request.GET.get('feeding_time', '').strip()
    diet = request.GET.get('diet', '').strip()
    medical_needs = request.GET.get('medical_needs', '').strip()
    zookeepers = request.GET.get('zookeepers', '').strip()
    
    if not feeding_time:
        return JsonResponse({"error": "Feeding time is required."}, status=400)
    if not diet:
        return JsonResponse({"error": "Diet is required."}, status=400)
    if not zookeepers:
        return JsonResponse({"error": "At least one zookeeper must be assigned."}, status=400)
    
    try:
        routine = CareRoutine.create(
            feeding_time=feeding_time,
            diet=diet,
            medical_needs=medical_needs
        )
        
        zookeeper_names = [z.strip() for z in zookeepers.split(',')]
        found_zookeepers = Zookeeper.objects.filter(name__in=zookeeper_names)
        
        if len(found_zookeepers) != len(zookeeper_names):
            missing = set(zookeeper_names) - set(z.name for z in found_zookeepers)
            routine.delete()  
            return JsonResponse({
                "error": f"Some zookeepers were not found: {', '.join(missing)}"
            }, status=404)
        
        routine.zookeepers.set(found_zookeepers)
        
        return JsonResponse({
            "message": "Care routine created successfully!",
            "care_routine": {
                "id": routine.id,
                "feeding_time": routine.feeding_time.strftime('%H:%M'),
                "diet": routine.diet,
                "medical_needs": routine.medical_needs,
                "zookeepers": [zookeeper.name for zookeeper in routine.zookeepers.all()]
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def update_care_routine(request):
    routine_id = request.GET.get('id', '').strip()
    feeding_time = request.GET.get('feeding_time', '').strip()
    diet = request.GET.get('diet', '').strip()
    medical_needs = request.GET.get('medical_needs', '').strip()
    zookeepers = request.GET.get('zookeepers', '').strip()
    
    if not routine_id:
        return JsonResponse({"error": "Care routine ID is required."}, status=400)
    
    try:
        routine_id = int(routine_id)
        routine = get_object_or_404(CareRoutine, id=routine_id)
        
        if feeding_time:
            routine.feeding_time = feeding_time
        if diet:
            routine.diet = diet
        if medical_needs:
            routine.medical_needs = medical_needs
            
        routine.save()
        
        if zookeepers:
            zookeeper_names = [z.strip() for z in zookeepers.split(',')]
            found_zookeepers = Zookeeper.objects.filter(name__in=zookeeper_names)
            
            if len(found_zookeepers) != len(zookeeper_names):
                missing = set(zookeeper_names) - set(z.name for z in found_zookeepers)
                return JsonResponse({
                    "error": f"Some zookeepers were not found: {', '.join(missing)}"
                }, status=404)
            
            if not found_zookeepers:
                return JsonResponse({
                    "error": "At least one zookeeper must be assigned to the care routine."
                }, status=400)
                
            routine.zookeepers.set(found_zookeepers)
        
        return JsonResponse({
            "message": f"Care routine {routine_id} updated successfully!",
            "updated_care_routine": {
                "id": routine.id,
                "feeding_time": routine.feeding_time.strftime('%H:%M'),
                "diet": routine.diet,
                "medical_needs": routine.medical_needs,
                "zookeepers": [zookeeper.name for zookeeper in routine.zookeepers.all()]
            }
        }, status=200)
    except ValueError:
        return JsonResponse({"error": "Care routine ID must be a valid integer."}, status=400)
    except CareRoutine.DoesNotExist:
        return JsonResponse({"error": f"No care routine found with the ID {routine_id}."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def delete_care_routine(request):
    routine_id = request.GET.get('id', '').strip()
    
    if not routine_id:
        return JsonResponse({"error": "Care routine ID is required to delete the care routine."}, status=400)
    
    try:
        routine_id = int(routine_id)
        routine = get_object_or_404(CareRoutine, id=routine_id)
        routine.delete()
        return JsonResponse({"message": f"Care routine {routine_id} deleted successfully!"}, status=200)
    except ValueError:
        return JsonResponse({"error": "Care routine ID must be a valid integer."}, status=400)
    except CareRoutine.DoesNotExist:
        return JsonResponse({"error": f"No care routine found with the ID {routine_id}."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def get_care_routine_detail(request, routine_id):
    try:
        routine_id = int(routine_id)
        routine = get_object_or_404(CareRoutine, id=routine_id)
        zookeepers = [
            {
                "id": zookeeper.id,
                "name": zookeeper.name
            }
            for zookeeper in routine.zookeepers.all()
        ]
        
        data = {
            "id": routine.id,
            "feeding_time": routine.feeding_time.strftime('%H:%M'),
            "diet": routine.diet,
            "medical_needs": routine.medical_needs,
            "zookeepers": zookeepers
        }
        return JsonResponse(data)
    except ValueError:
        return JsonResponse({"error": "Care routine ID must be a valid integer."}, status=400)
    except CareRoutine.DoesNotExist:
        return JsonResponse({"error": f"No care routine found with the ID {routine_id}."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)