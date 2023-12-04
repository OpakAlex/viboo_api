from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Room
from ..serializers import RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['GET'])
    def room_list(self, request):
        building_id = request.query_params.get('building_id')
        if building_id:
            rooms = Room.objects.filter(building__id=building_id)
        else:
            rooms = Room.objects.all()

        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def room_detail(self, request, pk=None):
        room = self.get_object()
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def room_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['PATCH'])
    def room_update(self, request, pk=None):
        room = self.get_object()
        serializer = self.get_serializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['DELETE'])
    def room_delete(self, request, pk=None):
        room = self.get_object()
        room.delete()
        return Response(status=204)
