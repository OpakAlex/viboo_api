from django.db import models
from .building import Building
from .room import Room

class Temperature(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.building.name} - {self.room.name} - {self.temperature}C @ {self.timestamp}"
