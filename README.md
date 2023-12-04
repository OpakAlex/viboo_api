# API Project

Welcome to the API project, a Django-based application designed to manage building information, rooms, and temperature records.

## Project Structure

The project is organized into a Django app named "temperature" within the "api" project.

    api/
    |-- temperature/
    | |-- migrations/
    | |-- __init__.py
    | |-- apps.py
    | |-- models
    | | |-- __init__.py
    | | |-- building.py
    | | |-- room.py
    | | |-- temperature.py
    | |--- __init__.py
    | |-- serializers
    | | |-- __init__.py
    | | |-- average_temperature_serializer.py
    | | |-- building_serializer.py
    | | |-- room_serializer.py
    | | |-- temperature_serializer.py
    | |-- views
    | | |-- __init__.py
    | | |-- building_views.py
    | | |-- room_views.py
    | | |-- temperature_views.py
    | |-- tests
    | | |-- __init__.py
    | | |-- views
    | | | |-- __init__.py
    | | | |-- test_building_views.py
    | | | |-- test_room_views.py
    | | | |-- test_temperature_views.py
    |-- api/
    | |-- init.py
    | |-- settings.py
    | |-- urls.py
    | |-- wsgi.py
    |-- manage.py
    |-- README.md
    |-- requirements.txt
    |-- data.sh

## Install
* pip install -r requirements.txt
* python manage.py migrate
* TEMPERATURE_APP_TOKEN="default_token_temperature_app" python manage.py runserver
* `./data.sh` to populate the database with sample data and see response examples.

## Configuration
1 .Set up your Django settings in api/api/settings.py.
2 .Configure the TEMPERATURE_APP_TOKEN middleware for authentication.

## Endpoints

### Building Endpoint

- **Endpoint:** `/api/v1/buildings/`
- **Methods:**
  - **POST:** Create a new building with details like name, address, and description.
  - **GET:** Retrieve a list of all buildings.
  - **PUT/PATCH:** Update details of an existing building.
  - **DELETE:** Delete an existing building.

### Room Endpoint

- **Endpoint:** `/api/v1/rooms/`
- **Methods:**
  - **POST:** Create a new room associated with a building, including details like name, floor, and building ID.
  - **GET:** Retrieve a list of all rooms.
  - **PUT/PATCH:** Update details of an existing room.
  - **DELETE:** Delete an existing room.

### Temperature Endpoint

- **Endpoint:** `/api/v1/temperatures/`
- **Methods:**
  - **POST:** Record temperature information associated with a building and room, including temperature value.
  - **GET:** Retrieve a list of all temperature records.
  - **PUT/PATCH:** Update details of an existing temperature record.
  - **DELETE:** Delete an existing temperature record.

### Average Temperature Endpoint

- **Endpoint:** `/api/v1/average_temperature/`
- **Method:** GET
- **Description:** Retrieve the average temperature for a specified building, room, and time duration.

## Custom Middleware

The project includes custom middleware for token-based authentication between microservices applications. Configure the `TEMPERATURE_APP_TOKEN` for secure communication.

## Docker

To run the project using Docker, follow these steps:

1. Build the Docker image:

   ```bash
   docker build -t api_project .
   ```

2. `docker run -p 8000:8000 api_project`


## Database
This project uses SQLite for development. For production, it's recommended to use PostgreSQL. Below is an example Python configuration for a PostgreSQL database with environment variables:

```python
# api/api/settings.py

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'your_database_name'),
        'USER': os.environ.get('DB_USER', 'your_database_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_database_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# CI/CD

This project follows a Continuous Integration (CI) workflow to ensure the reliability of the codebase.

## Continuous Integration (CI)

The CI process involves building a Docker image, setting up a PostgreSQL container, and running tests to ensure code quality and functionality.

### CI Steps

1. **Build Docker Image:**
   - Build the Docker image using the provided Dockerfile.

   ```bash
   docker build -t api_project .
   ```
2. **Set up PostgreSQL Container:**
   ```bash
   docker run -d --name postgres_for_tests -e POSTGRES_DB=test_db -e POSTGRES_USER=test_user -e POSTGRES_PASSWORD=test_password -p 5432:5432 postgres
   ```
3. **Run Tests:**
   ```bash
   docker run --rm --name api_tests --link postgres_for_tests -e DB_NAME=test_db -e DB_USER=test_user -e DB_PASSWORD=test_password -e DB_HOST=postgres_for_tests -e DB_PORT=5432 api_project python manage.py test
    ```

# Deployment

This section outlines the deployment process for the API project, including suggestions for using Helm charts with Kubernetes.

## Helm Chart

[Helm](https://helm.sh/) is a package manager for Kubernetes that provides an easy way to define, install, and upgrade even the most complex Kubernetes applications. It uses charts, which are packages of pre-configured Kubernetes resources.

### Custom Helm Chart

For this project, it's recommended to create a custom Helm chart to simplify the deployment process. A Helm chart can include configurations for both web deployment and custom job deployment.

Learn more about Helm charts [here](https://helm.sh/docs/topics/charts/).

### Web Deployment

For web deployment, your Helm chart can define Kubernetes resources such as Deployments, Services, and Ingress. This allows you to scale the web application easily.

### Custom Job Deployment

Custom job deployment, such as running database migrations, can be handled using Helm Jobs. A Helm Job allows you to run a set of pods to completion before considering the release as successful. This is useful for scenarios like running database migrations before deploying a new version of the web application.

## CI/CD Deployment Process

The CI/CD process for deploying this application involves running migrations via a Helm Job chart, waiting until the job is done (or a specified timeout), and then starting the Helm deployment.

### CI/CD Steps

1. **Run Migrations via Helm Job:**
   - Define a Helm Job chart that runs database migrations.

   ```bash
   helm install --name api-migrations ./charts/migrations
   ```
2. **Wait for Job to Complete:**
   ```bash
    kubectl wait --for=condition=complete job/api-migrations --timeout=900s
   ```
3. **Deploy Web Application:**
   ```bash
    helm install --name api-deployment ./charts/web
    ```
4. **Delete migrations job: **
    ```bash
    helm delete api-migrations
    ```
