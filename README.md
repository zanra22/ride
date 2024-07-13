# Python/Django Developer Test
## Objective
Create a RESTful API using Django REST Framework for managing ride information.

## Project Overview
This project implements a RESTful API using Django REST Framework (DRF) to manage ride information. The API supports creating, retrieving, updating, and deleting ride records and ride events, and it provides endpoints for generating detailed ride reports.

## Features
* **Ride Management**: CRUD Operations on ride records
* **User Management**: CRUD Operations on user records
* **Ride Report**: Generate reports on ride durations and driver performance

## Installation
#### Prerequisites
* Python 3.12.x
* Django 5.0
* Django REST Framework
#### Install Dependencies
*pip install -r requirements.txt*

#### Apply Migrations
*py manage.py migrate*

#### Create Superuser (For accessing Django Admin)
*py manage.py createsuperuser*

#### Run the development server
*py manage.py runserver*


# Usage
## API Endpoints
### Ride Endpoints
#### Create a ride
* URL: `rides/`
* Method: `POST`

#### Retrieve All Rides
* URL: `rides/`
* Method: `GET`

#### Retrieve a Specific Ride
* URL: `rides/{id}/`
* Method: `GET`

#### Update a Ride
* URL: `rides/{id}/`
* Method: `PUT`


#### Delete a Ride
* URL: `rides/{id}/`
* Method: `DELETE`


### Ride Event Endpoints
#### Create a Ride Event for a Ride
* URL: `rides/{id]/event/`
* Method: `POST`

#### Retrieve Ride Events for a Ride
* URL: `rides/{id]/event/`
* Method: `GET`

#### Retrieve a Specific Ride Event
* URL: `rides/{id]/event/{id}`
* Method: `GET`

#### Update a Ride Event
* URL: `rides/{id]/event/{id}`
* Method: `PUT`

#### Delete a Ride Event
* URL: `rides/{id]/event/{id}`
* Method: `DELETE`


### Report Endpoints
#### Retrieve trip report
* URL: `reports/`
* Method: `GET`

### User Endpoints
#### Retrieve users
* URL: `user/`
* Method: `GET`

#### Create user
* URL: `user/`
* Method: `POST`

#### Update user
* URL: `user/{id}`
* Method: `PUT`

#### Delete user
* URL: `user/{id}`
* Method: `PUT`


# Important Notice
#### All core requirements were "somehow" made. Apparently, one of the requirements is missing in this project, which is the sorting capability using distance to pickup. The approach I was trying is to use gis which is available in Django, however, upon proceeding, I faced a problem in which I spent a lot of time trying to make it work. The problem is related to GDAL. Somehow, even after installing GDAL through OSGeo4W and configuring the project to use the required directory, I still faced a problem in which, to be honest, exhausted my solutions.

#### Regarding the bonus requirement, I tried my best to try and achieve the sample output provided. However, based upon research, I need to change some of the things in the SQL query, since I used SQLite3 in this project. So what I did is create a function for the generating trip report which was included above. With that being said, I still tried to generate a SQL query in which gives back the data asked on the sample.

#### SQL Query:
    WITH RideDurations AS (
    SELECT
        r.id_driver_id AS driver_id,
        u.first_name || ' ' || u.last_name AS driver_name,
        strftime('%Y-%m', r.pickup_time) AS month,
        r.id_ride,
        MIN(CASE WHEN re.description = 'Status changed to pickup' THEN re.created_at END) AS pickup_time,
        MIN(CASE WHEN re.description = 'Status changed to dropoff' THEN re.created_at END) AS dropoff_time
    FROM rides_ride AS r
    INNER JOIN rides_rideevent AS re ON r.id_ride = re.id_ride_id
    INNER JOIN accounts_user AS u ON r.id_driver_id = u.id_user
    WHERE re.description IN ('Status changed to pickup', 'Status changed to dropoff')
    GROUP BY r.id_driver_id, u.first_name, u.last_name, strftime('%Y-%m', r.pickup_time), r.id_ride
    ),
    FilteredRides AS (
        SELECT
            driver_id,
            driver_name,
            month,
            id_ride,
            pickup_time,
            dropoff_time,
            (julianday(dropoff_time) - julianday(pickup_time)) * 24 AS duration_hours
        FROM RideDurations
        WHERE pickup_time IS NOT NULL AND dropoff_time IS NOT NULL
        )
    SELECT
        month,
        driver_name,
        COUNT(id_ride) AS trip_count
        FROM FilteredRides
        WHERE duration_hours > 1
        GROUP BY month, driver_name
        ORDER BY month, driver_name;

