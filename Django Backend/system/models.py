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
    
class Species(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def create(cls, name):
        species = cls(
            name=name,
        )
        species.save()
        return species



class Animal(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Changed from species to name
    species = models.ForeignKey(Species, on_delete=models.PROTECT, related_name='animals')
    diet = models.CharField(max_length=100)
    lifespan = models.PositiveIntegerField()
    behaviour = models.CharField(max_length=500)
    habitat = models.ManyToManyField(Habitat)
    
    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def create(cls, name, species, diet, lifespan, behaviour):
        animal = cls(
            name=name,
            species=species,
            diet=diet,
            lifespan=lifespan,
            behaviour=behaviour,
        )
        animal.save()
        return animal


    
class Zookeeper(models.Model):
    name = models.CharField(max_length=50, unique=True)
    qualification = models.CharField(max_length=100)
    responsibilities = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def create(cls, name, qualification, responsibilities):
        zookeeper = cls(
            name=name,
            qualification=qualification,
            responsibilities=responsibilities,
        )
        zookeeper.save()
        return zookeeper
    
class CareRoutine(models.Model):
    feeding_time = models.TimeField()
    diet = models.CharField(max_length=100)
    medical_needs = models.TextField(blank=True)
    zookeepers = models.ManyToManyField(Zookeeper, related_name='care_routines')
    
    def __str__(self):
        return f"Care Routine ({self.id}): {self.feeding_time}"
    
    @classmethod
    def create(cls, feeding_time, diet, medical_needs=""):
        routine = cls(
            feeding_time=feeding_time,
            diet=diet,
            medical_needs=medical_needs,
        )
        routine.save()
        return routine
    
    def add_zookeeper(self, zookeeper):
        self.zookeepers.add(zookeeper)
        
    def remove_zookeeper(self, zookeeper):
        self.zookeepers.remove(zookeeper)



