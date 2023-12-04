from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ...models import Building, Room, Temperature
import os

class TemperatureTests(TestCase):
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

        self.temperature_data = {
            'building': self.building,
            'room': self.room,
            'temperature': 25.5,
        }
        self.temperature = Temperature.objects.create(**self.temperature_data)

        self.url = reverse('temperature-detail', args=[self.temperature.id])
        self.token = os.environ.get('TEMPERATURE_APP_TOKEN')

    def add_auth_header(self, request):
        if self.token:
            request['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        return request

    def test_get_temperature_list(self):
        response = self.client.get(reverse('temperature-list'), **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_temperature_detail(self):
        response = self.client.get(self.url, **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['temperature'], self.temperature_data['temperature'])

    def test_create_temperature(self):
        initial_temperature_count = Temperature.objects.count()
        temperature_data = {
            'building': self.building.id,
            'room': self.room.id,
            'temperature': 26.0,
        }

        response = self.client.post('/api/v1/temperatures/', temperature_data, format='json', **self.add_auth_header({}))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Temperature.objects.count(), initial_temperature_count + 1)

    def test_update_temperature(self):
        updated_data = {
            'temperature': 27.0,
        }
        response = self.client.patch(self.url, updated_data, format='json', **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.temperature.refresh_from_db()
        self.assertEqual(self.temperature.temperature, updated_data['temperature'])

    def test_delete_temperature(self):
        response = self.client.delete(self.url, **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Temperature.objects.count(), 0)

    def test_average_temperature(self):
        response = self.client.get('/api/v1/average_temperature/', **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions based on your expected behavior for average temperature endpoint
