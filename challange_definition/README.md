# RoomPriceGenie

## Task description

You will be asked to implement two modules: Data Provider and the Dashboard Service. You can use any framework for both modules, however using FastAPI/Django/Flask is preferred. Below you can find the description of the modules and the requirements for each of them.

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

- `GET /events` - returns a list of events happened within a particular hotel. The list should be sorted by the timestamp in ascending order. The following query parameters should be supported:
  - `hotel_id` - the ID of the hotel
  - `updated__gte` - the start date of the event
  - `updated__lte` - the end date of the event
  - `rpg_status` - the status of the event (1 - booking, 2 - cancellation)
  - `room_id` - the ID of the room
  - `night_of_stay__gte` - the start date of stay
  - `night_of_stay__lte` - the end date of stay

- `POST /events` - creates a new event. The event should be validated according to the schema above. The event should be saved to the database.

### Dashboard Service

The Dashboard Service is a service that provides the following information: 
- The monthly number of bookings for a particular hotel for the year of choice
- The daily number of bookings for a particular hotel for the year of choice

The Dashboard Service should provide the following endpoints:

- `GET /dashboard` - returns the dashboard information for a particular hotel. The following query parameters should be supported:
  - `hotel_id` - the ID of the hotel
  - `period` - the period of the dashboard. The following values are supported:
    - `month` - the monthly dashboard
    - `day` - the daily dashboard
    - `year` - the year of the dashboard

## End goal
1. Some data has to be periodically added to the Data Provider’s database using `POST /events` endpoint - this is basically a simulation of data coming from the hotel into the booking management system.
2. There needs to be a periodic task that fills in the Dashboard Service’s database using the Data Provider’s `GET /events` endpoint. The data should be requested based on the event’s timestamp (please, reference the request parameters).
3. We should be able to trigger the `GET /dashboard` endpoint through Swagger and get the necessary data.

## Requirements
- Tests should have mocks for external services (keep in mind that the Data Provider is an external service for the Dashboard Service)
- Swagger/OpenAPI documentation should be provided for both modules
- Dockerized solution should be provided (with docker-compose)

## Data
You can find the sample data for the Data Provider [here](https://drive.google.com/file/d/14yZfUxcsNsHMxXS-b9ZKNWwKUpv9Wfk6/view?usp=sharing)