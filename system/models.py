from django.db import models

class Habitat(models.Model):
    name = models.CharField(max_length=50, unique=True, default='Savanna Plains')
    size = models.CharField(max_length=100, null=True, blank=True)
    climate = models.CharField(max_length=50, null=True, blank=True)
    suitable_species = models.TextField(null=True, blank=True)


class Animal(models.Model):
    DIET = [
        ('Herbivore', 'Herbivore'),
        ('Carnivore', 'Carnivore'),
        ('Omnivore', 'Omnivore'),
    ]

    name = models.CharField(max_length=50, null=True, default=None)
    diet = models.CharField(max_length=20, choices=DIET, default='Herbivore')
    lifespan = models.IntegerField(null=True, blank=True)
    behavior = models.TextField(null=True, blank=True)
    habitat = models.ForeignKey(Habitat, on_delete=models.SET_NULL, null=True, related_name='animals')
