# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code to the container
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the Django server using Gunicorn
CMD ["gunicorn", "roompricegenie.wsgi:application", "--bind", "0.0.0.0:8000"]
