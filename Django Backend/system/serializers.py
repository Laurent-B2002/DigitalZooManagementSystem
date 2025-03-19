from rest_framework import serializers
from .models import Habitat, Animal, Zookeeper, Task, Membership, Visitor, Event, EventFeedback

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

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class VisitorSerializer(serializers.ModelSerializer):
    membership = serializers.PrimaryKeyRelatedField(
        queryset=Membership.objects.all(), allow_null=True
    )
    class Meta:
        model = Visitor
        fields = ['id', 'name', 'email', 'password', 'membership', 'membership_start', 'membership_end']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventFeedbackSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    visitor = VisitorSerializer()
    class Meta:
        model = EventFeedback
        fields = '__all__'