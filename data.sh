#!/bin/bash

# Set your Django application base URL
BASE_URL="http://localhost:8000"

# Set the token for authentication
TOKEN="default_token_temperature_app"

# Create a building
BUILDING_RESPONSE=$(curl -X POST -H "AUTHORIZATION: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name": "Sample Building", "address": "123 Main St", "description": "Sample description"}' "$BASE_URL/api/v1/buildings/")
BUILDING_ID=$(echo $BUILDING_RESPONSE | jq -r '.id')

# # Create 3 rooms for the building
for i in {1..3}; do
  ROOM_RESPONSE=$(curl -X POST -H "AUTHORIZATION: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"building\": $BUILDING_ID, \"name\": \"Room $i\", \"floor\": $i}" "$BASE_URL/api/v1/rooms/")
  ROOM_ID=$(echo $ROOM_RESPONSE | jq -r '.id')

#   # Create 10 temperatures for each room
  for j in {1..10}; do
    RANDOM_TEMPERATURE=$(awk -v min=18 -v max=30 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')

    TEMPERATURE_RESPONSE=$(curl -X POST -H "AUTHORIZATION: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"building\": $BUILDING_ID, \"room\": $ROOM_ID, \"temperature\": $RANDOM_TEMPERATURE}" "$BASE_URL/api/v1/temperatures/")
    echo "Created temperature for Room $i: $TEMPERATURE_RESPONSE"
  done
done

# # Get average temperature for the building and room
AVERAGE_TEMPERATURE_RESPONSE=$(curl -X GET -H "AUTHORIZATION: Bearer $TOKEN" -H "Content-Type: application/json" "$BASE_URL/api/v1/average_temperature/?building_id=$BUILDING_ID&room_id=$ROOM_ID&minutes=15")
echo "Average Temperature: $AVERAGE_TEMPERATURE_RESPONSE"
