# RoomPriceGenie Assignment

## Assignment Description

Please check the [challange_definition](./challange_definition) folder.


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

### 1. Cloning the Repository

First, clone the GitHub repository to your local machine:

```sh
git clone git@github.com:arkeodev/roompricegenie.git
```

```sh
cd roompricegenie
```

### 2. Build Docker Containers

Build the Docker containers:

```sh
docker-compose build
```

### 3. Start Redis and Web Service

Start the Redis and Web service containers (but not the Celery containers yet):

```sh
docker-compose up -d redis web
```

### 4. Apply Migrations

Run migrations for the `data_provider` database:

```sh
docker-compose run web bash -c "poetry run python manage.py migrate --database=data_provider"
```

Run migrations for the `dashboard_service` database:

```sh
docker-compose run web bash -c "poetry run python manage.py migrate --database=dashboard_service"
```

### 5. Run Tests

Run the tests using `pytest`:

```sh
docker-compose run web bash -c "poetry run pytest"
```

### 6. Test Event API

Test Event API to verify that the service is working correctly. 

Check that I'm using year 2019 in the below call, because incoming data from the data.csv file is greater than this year and it allows us to run the tasks.

```sh
curl -X POST http://localhost:8000/events/ -H "Content-Type: application/json" -d '{"hotel_id": 1, "event_timestamp": "2019-01-01T00:00:00Z", "status": 1, "room_reservation_id": "0013e338-0158-4d5c-8698-aebe00cba360", "night_of_stay": "2019-01-01"}'
```

```sh
curl -X GET http://localhost:8000/events/?hotel_id=1
```

### 7. Start Celery Workers

Once the databases are set up, start the Celery workers in the order below and beat service. 

Start the Celery event processing task worker:
```sh
docker-compose up -d celery
```

Start the Celery dashboard generation task worker:
```sh
docker-compose up -d celery-update
```

This command is pushing all the data into a Redis queue.
```sh
docker-compose run web bash -c "poetry run python manage.py trigger_load_events"
```

Start the Celery beat service:
```sh
docker-compose up -d celery-beat
```

### 8. Access the Application

[Access the application root page from a browser](http://localhost:8000)

[Access the Swagger documentation page from a browser](http://localhost:8000/swagger/)

In swagger you can test the the **Dashboard API**

---

## Local Installation and Usage

### 1. Cloning the Repository

First, clone the GitHub repository to your local machine:

```sh
git clone https://github.com/arkeodev/roompricegenie.git

cd roompricegenie
```

### 2. Preparing the Environment

Ensure you have [Poetry](https://python-poetry.org/) installed for dependency management. Then, install the dependencies:

```sh
poetry install
```

### 3. Preparing the Databases

Run the following commands to prepare your databases:\

```sh
cd roompricegenie
```

```sh
poetry run python manage.py migrate --database=data_provider
poetry run python manage.py migrate --database=dashboard_service
```

### 4. Running the Application

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
    poetry run celery -A roompricegenie worker -l info -Q dashboard_queue -c 1
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

## Running Unit Tests

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
