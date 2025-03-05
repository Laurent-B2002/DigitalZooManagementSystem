from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from .models import Animal, Habitat, Zookeeper, Task
from rest_framework import viewsets
from .serializers import HabitatSerializer, AnimalSerializer, ZookeeperSerializer, TaskSerializer
from django.core.mail import send_mail
from django.conf import settings

class HabitatViewSet(viewsets.ModelViewSet):
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class ZookeeperViewSet(viewsets.ModelViewSet):
    queryset = Zookeeper.objects.all()
    serializer_class = ZookeeperSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        data = self.request.data
        zookeeper_name = data.get("zookeeper")
        animal_species = data.get("animal")

        try:
            zookeeper = Zookeeper.objects.get(name=zookeeper_name)
            animal = Animal.objects.get(species=animal_species)
        except Zookeeper.DoesNotExist:
            raise ValidationError({"error": f"Zookeeper '{zookeeper_name}' not found."})
        except Animal.DoesNotExist:
            raise ValidationError({"error": f"Animal '{animal_species}' not found."})

        task = serializer.save(zookeeper=zookeeper, animal=animal)

        send_mail(
            subject=f"New Task: {task.task_type}",
            message=f"Hello {task.zookeeper.name},\n\nYou have been assigned a new task:\n\n"
                    f"Animal: {task.animal.species}\n"
                    f"Task Type: {task.get_task_type_display()}\n"
                    f"Description: {task.description}\n"
                    f"Scheduled Time: {task.scheduled_time}\n\n"
                    f"Please complete it on time.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[task.zookeeper.email],
        )


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
    

def delete_zookeeper(request):
    name = request.GET.get('name', '').strip()
    
    if not name:
        return JsonResponse({"error": "Name is required to delete the zookeeper."}, status=400)
    
    try:
        zookeeper = get_object_or_404(Zookeeper, name=name)
        zookeeper.delete()
        return JsonResponse({"message": f"Zookeeper '{name}' deleted successfully!"}, status=200)
    except Animal.DoesNotExist:
        return JsonResponse({"error": f"No zookeeper found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    
def update_zookeeper(request):
    name = request.GET.get('name', '').strip()
    new_name = request.GET.get('new_name', '').strip()
    role = request.GET.get('role', '').strip()
    email = request.GET.get('email', '').strip()

    if not name:
        return JsonResponse({"error": "Current zookeeper name is required to identify the zookeeper."}, status=400)
    
    try:
        zookeeper = get_object_or_404(Zookeeper, name=name)
        
        if new_name:
            if Zookeeper.objects.filter(name=new_name).exists() and new_name != name:
                return JsonResponse({"error": f"Zookeeper with name '{new_name}' already exists."}, status=400)
            zookeeper.name = new_name
        
        if role:
            if role not in dict(Zookeeper.ROLE_TYPES).keys():
                return JsonResponse({"error": f"Invalid role. Available roles are: {', '.join(dict(Zookeeper.ROLE_TYPES).keys())}"}, status=400)
            zookeeper.role = role
            
        if email:
            if Zookeeper.objects.filter(email=email).exists() and email != zookeeper.email:
                return JsonResponse({"error": f"A zookeeper with email '{email}' already exists."}, status=400)
            zookeeper.email = email
        
        zookeeper.save()
        
        return JsonResponse({
            "message": f"Zookeeper '{name}' updated successfully!",
            "updated_zookeeper": {
                "id": zookeeper.id,
                "name": zookeeper.name,
                "role": zookeeper.role,
                "email": zookeeper.email
            }
        }, status=200)
    
    except Zookeeper.DoesNotExist:
        return JsonResponse({"error": f"No zookeeper found with the name '{name}'."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
