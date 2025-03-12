from django.contrib import admin
from .models import Habitat, Animal, Zookeeper, Task, Membership, Visitor, Event, EventFeedback
# Register your models here.

admin.site.register(Habitat)
admin.site.register(Animal)
admin.site.register(Zookeeper)
admin.site.register(Task)
admin.site.register(Membership)
admin.site.register(Visitor)
admin.site.register(Event)
admin.site.register(EventFeedback)