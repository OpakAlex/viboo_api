from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import health_check
from .views import BuildingViewSet, RoomViewSet, TemperatureViewSet

building_router = DefaultRouter()
building_router.register(r'buildings', BuildingViewSet, basename='building')

room_router = DefaultRouter()
room_router.register(r'rooms', RoomViewSet, basename='room')

temperature_router = DefaultRouter()
temperature_router.register(r'temperatures', TemperatureViewSet, basename='temperature')

urlpatterns = [
        path('api/v1/', include(building_router.urls)),
        path('api/v1/', include(room_router.urls)),
        path('api/v1/', include(temperature_router.urls)),
        path('api/v1/average_temperature/', TemperatureViewSet.as_view({'get': 'average_temperature'}), name='average_temperature'),
        ]
