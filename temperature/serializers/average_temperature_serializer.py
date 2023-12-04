from rest_framework import serializers

class AverageTemperatureSerializer(serializers.Serializer):
    average_temperature = serializers.FloatField()
