## Project Overview

The RoomPriceGenie project involves developing two modules: the Data Provider and the Dashboard Service. The Data Provider module simulates hotel booking and cancellation events, while the Dashboard Service aggregates this data to provide insights on bookings. This project is implemented using Django and includes REST APIs, Celery for asynchronous tasks, and Docker for containerization.

## Tech Stack and Roles

- **Django**: The primary framework for building the web application, handling the API endpoints, ORM for database interactions, and the admin interface.
- **Django REST Framework**: Provides powerful and flexible tools for building RESTful APIs.
- **Celery**: An asynchronous task queue/job queue used to manage periodic tasks for data simulation and dashboard updates.
- **Redis**: Used as the message broker for Celery to handle task queues.
- **PostgreSQL/SQLite**: PostgreSQL is recommended for production, while SQLite is used for development and testing to simplify setup.
- **Docker**: Containerizes the application, ensuring consistent environments across different deployment stages.
- **drf-yasg**: Automatically generates Swagger/OpenAPI documentation for the APIs.
- **Poetry**: Dependency management and packaging tool for Python projects.
- **Pytest**: Testing framework to ensure the code quality and functionality of the application.
- **Requests-mock**: Library for mocking HTTP requests in tests

## Installation

### Prerequisites

- Python 3.11
- Docker
- Poetry

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd roompricegenie
   ```

2. **Install Dependencies**:
   ```bash
   poetry install
   ```

3. **Run Migrations**:
   ```bash
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate
   ```

4. **Create a Superuser** (Optional for accessing the admin interface):
   ```bash
   poetry run python manage.py createsuperuser
   ```

## Usage

### Manual Usage

1. **Run the Development Server**:
   ```bash
   poetry run python manage.py runserver
   ```

2. **Access the Application**:
   - API Documentation: `http://127.0.0.1:8000/swagger/`
   - Admin Interface: `http://127.0.0.1:8000/admin/`

### Docker-Based Usage

1. **Build and Run Docker Containers**:
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**:
   - API Documentation: `http://127.0.0.1:8000/swagger/`
   - Admin Interface: `http://127.0.0.1:8000/admin/`

3. **Stop the Docker Containers**:
   ```bash
   docker-compose down
   ```

## Testing

### Running Tests

1. **Run All Tests**:
   ```bash
   poetry run pytest
   ```

2. **Test Structure**:
   - `data_provider/tests/test_models.py`: Tests for Data Provider models.
   - `data_provider/tests/test_serializers.py`: Tests for Data Provider serializers.
   - `data_provider/tests/test_views.py`: Tests for Data Provider views.
   - `dashboard_service/tests/test_models.py`: Tests for Dashboard Service models.
   - `dashboard_service/tests/test_serializers.py`: Tests for Dashboard Service serializers.
   - `dashboard_service/tests/test_views.py`: Tests for Dashboard Service views.
   - `dashboard_service/tests/test_tasks.py`: Tests for periodic tasks with mocking.

### Mocking External Services
Mocking is used in tests to simulate external service interactions, ensuring tests run in isolation and are not dependent on external systems. We use the unittest.mock module to mock HTTP requests in the tests for the Dashboard Service.


## Swagger Documentation

### Accessing Swagger UI

1. **Ensure the Server is Running**:
   ```bash
   poetry run python manage.py runserver
   ```

2. **Access Swagger UI**:
   Visit `http://127.0.0.1:8000/swagger/` in your browser to view the API documentation.