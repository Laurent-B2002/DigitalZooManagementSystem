from django.db import models

class Habitat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    size = models.CharField(max_length=100)
    climate = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def create(cls, name, size, climate):
        habitat = cls(
            name=name,
            size=size,
            climate=climate,
        )
        habitat.save()
        return habitat

class Animal(models.Model):
    species = models.CharField(max_length=50, unique=True)
    diet = models.CharField(max_length=100)
    lifespan = models.PositiveIntegerField()
    behaviour = models.CharField(max_length=500)
    habitat = models.ManyToManyField(Habitat)
    
    def __str__(self):
        return f"{self.species}"
    
    @classmethod
    def create(cls, species, diet, lifespan, behaviour):
        animal = cls(
            species=species,
            diet=diet,
            lifespan=lifespan,
            behaviour=behaviour,
        )
        animal.save()
        return animal

