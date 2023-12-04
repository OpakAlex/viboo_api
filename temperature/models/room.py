from django.db import models
from .building import Building

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    floor = models.IntegerField()

    def __str__(self):
        return f"{self.building.name} - {self.name}"
