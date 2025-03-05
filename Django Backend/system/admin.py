from django.contrib import admin
from .models import Habitat, Animal, Zookeeper, Task
# Register your models here.

admin.site.register(Habitat)
admin.site.register(Animal)
admin.site.register(Zookeeper)
admin.site.register(Task)