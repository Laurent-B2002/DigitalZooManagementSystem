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

class Zookeeper(models.Model):
    ROLE_TYPES = (
        ('L1', 'Level1'),
        ('L2', 'Level2'),
        ('L3', 'Level3'),
        ('admin', 'Admin'),
    )
    name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_TYPES, default='L1')
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.name}"

class Task(models.Model):
    TASK_TYPES = [
        ('FEEDING', 'Feeding'),
        ('MEDICAL', 'Medical'),
        ('CLEANING', 'Cleaning'),
        ('OTHER', 'Other'),
    ]
    zookeeper = models.ForeignKey(Zookeeper, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    description = models.TextField()
    scheduled_time = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_type} for {self.animal.species} by {self.zookeeper.name}"