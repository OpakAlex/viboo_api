from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ...models import Room, Building
import os

class RoomTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.building_data = {
            'name': 'Test Building',
            'address': 'Test Address',
            'description': 'Test Description',
        }
        self.building = Building.objects.create(**self.building_data)
        self.room_data = {
            'building': self.building,
            'name': 'Test Room',
            'floor': 1,
        }
        self.room = Room.objects.create(**self.room_data)
        self.url = reverse('room-detail', args=[self.room.id])
        self.token = os.environ.get('TEMPERATURE_APP_TOKEN')

    def add_auth_header(self, request):
        if self.token:
            request['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        return request

    def test_get_room_list(self):
        response = self.client.get(reverse('room-list'), **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_room_detail(self):
        response = self.client.get(self.url, **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.room_data['name'])

    def test_create_room(self):
        initial_room_count = Room.objects.count()
        room_data = {
            'building': self.building.id,
            'name': 'New Room',
            'floor': 2,
        }

        response = self.client.post('/api/v1/rooms/', room_data, format='json', **self.add_auth_header({}))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), initial_room_count + 1)

    def test_update_room(self):
        updated_data = {
            'name': 'Updated Room',
            'floor': 3,
        }
        response = self.client.patch(self.url, updated_data, format='json', **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.name, updated_data['name'])

    def test_delete_room(self):
        response = self.client.delete(self.url, **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.count(), 0)
