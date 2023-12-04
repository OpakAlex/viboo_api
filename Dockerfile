FROM python:3.12.0

# Set environment variables
ARG TEMPERATURE_APP_TOKEN

ENV TEMPERATURE_APP_TOKEN "default_token_temperature_app"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the default port for the Django development server
EXPOSE 8000

# Command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
