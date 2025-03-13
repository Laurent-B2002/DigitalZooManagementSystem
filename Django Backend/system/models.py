from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from dateutil.relativedelta import relativedelta
from datetime import datetime

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
    
class Membership(models.Model):
    ROLE_TYPES = (
        ('L1', 'Level1 Member'),
        ('L2', 'Level2 Member'),
        ('L3', 'Level3 Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_TYPES, default='L1')
    detail = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    duration = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.role}"
    
class Visitor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
    membership_start = models.DateField(null=True, blank=True)
    membership_end = models.DateField(null=True, blank=True)

    def renew(self):
        if self.membership:
            today = datetime.now().date()
            if self.membership_end and self.membership_end > today:
                self.membership_end += relativedelta(months=self.membership.duration)
            else:
                self.membership_start = today
                self.membership_end = today + relativedelta(months=self.membership.duration)
            self.save()

    def __str__(self):
        return f"{self.name}"

class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    time = models.DateTimeField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # attend = models.ManyToManyField(Visitor, related_name='events')
    memberships = models.ManyToManyField(Membership, related_name='events')

    def discounted(self, visitor):
        if visitor.membership and visitor.membership.discount:
            return self.price * visitor.membership.discount
        return self.price

    def __str__(self):
        return f"{self.name}"
    
class EventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"Feedback for {self.event.name} by {self.visitor.name} - {self.rating} Stars"
    
    