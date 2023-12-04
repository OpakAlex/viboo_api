from rest_framework import serializers
from ..models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'building', 'name', 'floor', 'created_at', 'updated_at']
