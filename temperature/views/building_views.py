from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Building
from ..serializers import BuildingSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    @action(detail=False, methods=['GET'])
    def building_list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def building_detail(self, request, pk=None):
        building = self.get_object()
        serializer = self.get_serializer(building)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def building_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['PATCH'])
    def building_update(self, request, pk=None):
        building = self.get_object()
        serializer = self.get_serializer(building, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['DELETE'])
    def building_delete(self, request, pk=None):
        building = self.get_object()
        building.delete()
        return Response(status=204)
