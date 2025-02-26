from django.db import models

class Habitat(models.Model):
    name = models.CharField(max_length=50, null=True, default=None)


class Animal(models.Model):
    name = models.CharField(max_length=50, null=True, default=None)
    habitat = models.ForeignKey(Habitat, on_delete=models.SET_NULL, null=True, related_name='animals')
