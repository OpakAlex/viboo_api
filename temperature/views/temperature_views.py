from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Temperature
from ..serializers import TemperatureSerializer, AverageTemperatureSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg

class TemperatureViewSet(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    @action(detail=False, methods=['GET'])
    def temperature_list(self, request):
        building_id = request.query_params.get('building_id')
        room_id = request.query_params.get('room_id')

        temperatures = Temperature.objects.all()

        if building_id:
            temperatures = temperatures.filter(building__id=building_id)

        if room_id:
            temperatures = temperatures.filter(room__id=room_id)

        serializer = self.get_serializer(temperatures, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def temperature_detail(self, request, pk=None):
        temperature = self.get_object()
        serializer = self.get_serializer(temperature)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def temperature_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['PATCH'])
    def temperature_update(self, request, pk=None):
        temperature = self.get_object()
        serializer = self.get_serializer(temperature, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['DELETE'])
    def temperature_delete(self, request, pk=None):
        temperature = self.get_object()
        temperature.delete()
        return Response(status=204)

    @action(detail=False, methods=['GET'])
    def average_temperature(self, request):
        building_id = request.query_params.get('building_id')
        room_id = request.query_params.get('room_id')
        minutes = int(request.query_params.get('minutes', 15))

        end_time = timezone.now()
        start_time = end_time - timezone.timedelta(minutes=minutes)

        temperatures = Temperature.objects.filter(
            timestamp__range=(start_time, end_time)
        )

        if building_id:
            temperatures = temperatures.filter(building__id=building_id)

        if room_id:
            temperatures = temperatures.filter(room__id=room_id)

        average_temperature = temperatures.aggregate(Avg('temperature'))['temperature__avg']
        serializer = AverageTemperatureSerializer({'average_temperature': average_temperature})

        return Response(serializer.data)
