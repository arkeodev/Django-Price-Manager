# RoomPriceGenie Assignment

## Assignment Description

It is asked to implement two modules: Data Provider and the Dashboard Service. It can be used any framework for both modules, however using FastAPI/Django/Flask is preferred. 

Here I preffered to use Django.

Below it can be found the description of the modules and the requirements for each of them.

### Data Provider

The Data Provider is a service that provides booking and cancellation events happening within a particular hotel. The following is an example of a single booking event:

```json
{
  "id": 1,
  "hotel_id": 1,
  "event_timestamp": "2020-01-01T00:00:00Z",
  "status": 1, // 1 - booking, 2 - cancellation
  "room_id": 1,
  "night_of_stay": "2020-01-01"
}
```

The Data Provider should provide the following endpoints:

- **GET /events** - returns a list of events happened within a particular hotel. The list should be sorted by the timestamp in ascending order. The following query parameters should be supported:
  - hotel_id - the ID of the hotel
  - updated__gte - the start date of the event
  - updated__lte - the end date of the event
  - rpg_status - the status of the event (1 - booking, 2 - cancellation)
  - room_id - the ID of the room
  - night_of_stay__gte - the start date of stay
  - night_of_stay__lte - the end date of stay

- **POST /events** - creates a new event. The event should be validated according to the schema above. The event should be saved to the database.

### Dashboard Service

The Dashboard Service is a service that provides the following information:
- The monthly number of bookings for a particular hotel for the year of choice
- The daily number of bookings for a particular hotel for the year of choice

The Dashboard Service should provide the following endpoints:

- **GET /dashboard** - returns the dashboard information for a particular hotel. The following query parameters should be supported:
  - hotel_id - the ID of the hotel
  - period - the period of the dashboard. The following values are supported:
    - month - the monthly dashboard
    - day - the daily dashboard
  - year - the year of the dashboard

## End Goal

1. Some data has to be periodically added to the Data Provider’s database using the POST /events endpoint - this is basically a simulation of data coming from the hotel into the booking management system.
2. There needs to be a periodic task that fills in the Dashboard Service’s database using the Data Provider’s GET /events endpoint. The data should be requested based on the event’s timestamp.
3. We should be able to trigger the GET /dashboard endpoint through Swagger and get the necessary data.

## Requirements

- Tests should have mocks for external services (keep in mind that the Data Provider is an external service for the Dashboard Service).
- Swagger/OpenAPI documentation should be provided for both modules.
- Dockerized solution should be provided (with docker-compose).

---

## Solution

RoomPriceGenie is designed as a comprehensive Django-based application that automates and optimizes room pricing strategies by leveraging real-time data processing and a responsive dashboard interface. Below is an overview of the key components and their roles within the system:

### Main Components

- **RoomPriceGenie Core**:
  - **Django ASGI & WSGI**: Configurations for asynchronous and synchronous web servers.
  - **Celery**: Used for handling asynchronous task queues to manage long-running processes without blocking the main server.
  - **Routers**: Defines URL route handlers that direct incoming requests to appropriate views.
  - **Settings**: Contains all configuration settings for the Django project, including database configurations, third-party apps, and middleware settings.
  - **URLs & Views**: Define the logic and endpoints for user interactions and API responses.

- **Dashboard Service**:
  - **Models**: Includes the `DashboardData` table, which stores metrics and statistics for display on the dashboard.
  - **Serializers**: Handle the conversion of model instances to JSON for API responses.
  - **Tasks**: Asynchronous tasks, such as the generation of dashboard metrics, are scheduled and executed.
  - **Admin**: Django admin configurations for managing dashboard data through a graphical interface.
  - **Tests**: Unit tests to ensure the reliability and integrity of dashboard functionalities.

- **Data Provider**:
  - **Management Commands**: Scripts to load external CSV data into a Redis queue, facilitating quick and efficient data handling.
  - **Models**: Contains the `Event` table to log and track data events processed by the system.
  - **Tasks**: Background tasks for loading events from the Redis queue into the database.
  - **Tests**: Comprehensive tests to validate data integrity and the correct functioning of data processing workflows.

### Infrastructure

- **Docker**: Utilizes Docker containers to encapsulate the application environment, ensuring consistency across different development and production setups.
- **Gunicorn**: Serves as the WSGI HTTP Server to run Python web applications from a Docker container, particularly suited for handling concurrent requests.
- **Poetry**: Manages dependencies and packages, providing a reproducible environment and simplifying package management and deployment.

### Setup and Deployment

- **Environment Setup**: Utilize the `.env` file to configure necessary environment variables such as database URLs, API keys, and other sensitive configurations. 
- **Docker Compose**: Simplifies the deployment of multi-container Docker applications, allowing each component of RoomPriceGenie to be launched with predefined settings.

### Static and Templates

- **Static**: Serves static files for the **root api** frontend.

---

## Project Structure

```
RoomPriceGenie/
│
├── .env                    # Environment variables for the project
├── gunicorn.conf.py        # Gunicorn configuration for Django
├── manage.py               # Django's command-line utility for administrative tasks
├── docker-compose.yml      # Docker configuration file
├── LICENSE                 # Project license
├── poetry.lock             # Poetry package versions lockfile
├── pyproject.toml          # Poetry configuration file
├── pytest.ini              # Pytest configuration file
├── README.md               # The file you are reading
│
├── roompricegenie/         # Main Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── routers.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
│
├── dashboard_service/      # Dashboard service module
│   ├── migrations/         # dashboard_service db migrations
│   ├── tests/              # Dashboard service unit tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py            # dashboard service generation task
│   ├── urls.py
│   └── views.py
│
├── data_provider/          # data provider module
│   ├── management/         # data provider commands
│   ├── migrations/         # data_provider db migrations
│   ├── tests/              # Data provider unit tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py            # data provider event loading tasks
│   ├── urls.py
│   └── views.py
│
├── static/                 # Static files for the web application
└── templates/              # Django templates directory
```

---

## Tech Stack and Roles

- **Django**: The primary framework for building the web application, handling the API endpoints, ORM for database interactions, and the admin interface.
- **Django REST Framework**: Provides powerful and flexible tools for building RESTful APIs.
- **Celery**: An asynchronous task queue/job queue used to manage periodic tasks for data simulation and dashboard updates.
- **Redis**: Used as the message broker for Celery to handle task queues.
- **PostgreSQL/SQLite**: PostgreSQL is recommended for production, while SQLite is used for development and testing to simplify setup. 

   **IMPORTANT**: Because it uses SQLite, there may be some db locks if the number of workers for Celery is increased. It is kept as 1.

- **Docker**: Containerizes the application, ensuring consistent environments across different deployment stages.
- **drf-yasg**: Automatically generates Swagger/OpenAPI documentation for the APIs.
- **Poetry**: Dependency management and packaging tool for Python projects.
- **Pytest**: Testing framework to ensure the code quality and functionality of the application.
- **Requests-mock**: Library for mocking HTTP requests in tests.

---

## Installation and Usage with Docker

The `depends_on` directive in Docker Compose ensures that the `celery` and `celery-beat` services start after the `redis` service, but it doesn't guarantee that the `web` service will be fully ready before starting `celery` and `celery-beat`.

To ensure `celery` and `celery-beat` start only after the `web` service is fully ready (i.e., after migrations are applied), we won't start them immediately with `docker-compose up`. Instead, we'll manually start them after setting up the databases.

Here's a step-by-step guide, including test API calls for each endpoint:

### 1. Build Docker Containers

Build the Docker containers:

```sh
docker-compose build
```

### 2. Start Redis and Web Service

Start the Redis and Web service containers (but not the Celery containers yet):

```sh
docker-compose up -d redis web
```

### 3. Apply Migrations

Run migrations for the `default` database:

```sh
docker-compose run web bash -c "poetry run python manage.py migrate --database=default"
```

Run migrations for the `data_provider` database:

```sh
docker-compose run web bash -c "poetry run python manage.py migrate --database=data_provider"
```

Run migrations for the `dashboard_service` database:

```sh
docker-compose run web bash -c "poetry run python manage.py migrate --database=dashboard_service"
```

### 4. Run Tests

Run the tests using `pytest`:

```sh
docker-compose run web bash -c "poetry run pytest"
```

### 5. Start Celery Workers

Once the databases are set up, start the Celery workers and beat service:

Start the Celery worker:

```sh
docker-compose up -d celery
```

Start the Celery beat service:

```sh
docker-compose up -d celery-beat
```

### 6. Access the Application

Access the application root page:

```sh
curl http://localhost:8000
```

Access the Swagger documentation page:

```sh
curl http://localhost:8000/swagger/
```

### 7. Test API Calls

Test API calls to verify that the services are working correctly.

#### Test Event API (3 sample calls):

```sh
curl -X POST http://localhost:8000/events/ -H "Content-Type: application/json" -d '{"hotel_id": 1, "timestamp": "2023-01-01T00:00:00Z", "rpg_status": 1, "room_reservation_id": "0013e338-0158-4d5c-8698-aebe00cba360", "night_of_stay": "2023-01-01"}'

curl -X GET http://localhost:8000/events/?hotel_id=1

curl -X GET http://localhost:8000/events/?hotel_id=1&updated_gte=2023-01-01T00:00:00Z
```

#### Test Dashboard API (3 sample calls):

```sh
curl -X GET http://localhost:8000/dashboard/?hotel_id=1&period=day&year=2023&month=1&day=1

curl -X GET http://localhost:8000/dashboard/?hotel_id=1&period=month&year=2023&month=1

curl -X GET http://localhost:8000/dashboard/?hotel_id=1&period=day&year=2023&month=1
```

---

## Local Installation and Usage

### Cloning the Repository

First, clone the GitHub repository to your local machine:

```sh
git clone https://github.com/arkeodev/roompricegenie.git

cd roompricegenie
```

### Preparing the Environment

Ensure you have [Poetry](https://python-poetry.org/) installed for dependency management. Then, install the dependencies:

```sh
poetry install
```

### Preparing the Databases

Run the following commands to prepare your databases:\

```sh
cd roompricegenie
```

```sh
poetry run python manage.py migrate --database=data_provider
poetry run python manage.py migrate --database=dashboard_service
```

### Running the Application

You'll need four different terminals for this process:

1. **Terminal 1: Running the app with Gunicorn**
   This command starts the gunicorn server.
    ```sh
    poetry run gunicorn roompricegenie.wsgi:application --bind 0.0.0.0:8000
   ```
2. **Terminal 3: Running Celery event processing task worker**
    This command starts the Celery event processing
    ```sh
    poetry run celery -A roompricegenie worker -l info -c 3
    ```

3. **Terminal 3: Running Celery dashboard generation task worker**
   This command starts the Celery dashboard generation task.
    ```sh
    celery -A roompricegenie worker -l info -Q dashboard_queue -c 1
    ```

4. **Terminal 2: Running Celery beat**
   This first command is pushing all the data into a Redis queue.
    ```sh
    poetry run python manage.py trigger_load_events
    ```

   This second command starts the periodic tasks.
    ```sh
    poetry run celery -A roompricegenie beat -l info
    ```

---

## Running Tests

1. **Run All Tests**:
   ```sh
   poetry run pytest
   ```

2. **Test Structure**:
   - `data_provider/tests/test_models.py`: Tests for Data Provider models.
   - `data_provider/tests/test_serializers.py`: Tests for Data Provider serializers.
   - `data_provider/tests/test_views.py`: Tests for Data Provider views.
   - `dashboard_service/tests/test_tasks.py`: Tests for Data Provider generation periodic tasks with mocking.
   - `dashboard_service/tests/test_models.py`: Tests for Dashboard Service models.
   - `dashboard_service/tests/test_serializers.py`: Tests for Dashboard Service serializers.
   - `dashboard_service/tests/test_views.py`: Tests for Dashboard Service views.
   - `dashboard_service/tests/test_tasks.py`: Tests for Dashboard periodic tasks with mocking.

### Mocking External Services

Mocking is used in tests to simulate external service interactions, ensuring tests run in isolation and are not dependent on external systems. We use the `unittest.mock` module to mock HTTP requests in the tests for the Dashboard Service.

---

## Swagger Documentation

### Accessing Swagger UI

1. **Ensure the Server is Running**:
   ```sh
   poetry run python manage.py runserver
   ```

2. **Access Swagger UI**:
   Visit [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) in your browser to view the API documentation.
