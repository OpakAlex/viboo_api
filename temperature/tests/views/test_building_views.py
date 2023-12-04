from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ...models import Building
import os

class BuildingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.building_data = {
            'name': 'Test Building',
            'address': 'Test Address',
            'description': 'Test Description',
        }
        self.building = Building.objects.create(**self.building_data)
        self.url = reverse('building-detail', args=[self.building.id])
        self.token = os.environ.get('TEMPERATURE_APP_TOKEN')

    def add_auth_header(self, request):
        if self.token:
            request['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        return request

    def test_get_building_list(self):
        response = self.client.get(reverse('building-list'), **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_building_detail(self):
        response = self.client.get(self.url, **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.building_data['name'])

    def test_create_building(self):
        initial_building_count = Building.objects.count()
        building_data = {
            'name': 'New Building',
            'address': 'New Address',
            'description': 'New Description',
        }

        response = self.client.post('/api/v1/buildings/', building_data, format='json', **self.add_auth_header({}))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Building.objects.count(), initial_building_count + 1)

    def test_update_building(self):
        updated_data = {
            'name': 'Updated Building',
            'address': 'Updated Address',
            'description': 'Updated Description',
        }
        response = self.client.patch(self.url, updated_data, format='json', **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.building.refresh_from_db()
        self.assertEqual(self.building.name, updated_data['name'])

    def test_delete_building(self):
        response = self.client.delete(self.url, **self.add_auth_header({}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Building.objects.count(), 0)
