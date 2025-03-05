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
    class Meta:
        model = Task
        fields = '__all__'
