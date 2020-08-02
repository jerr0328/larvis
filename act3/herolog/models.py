from django.db import models
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class WorldSave(models.Model):
    how = models.TextField()
    who = models.ManyToManyField(Person, blank=True)
    when = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.when)
