from rest_framework import serializers
from .models import Habitat, Animal, Zookeeper, Task

class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

class ZookeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zookeeper
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    zookeeper_name = serializers.CharField(source="zookeeper.name", read_only=True)
    animal_species = serializers.CharField(source="animal.species", read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task_type', 'description', 'scheduled_time', 'completed', 'zookeeper_name', 'animal_species']
