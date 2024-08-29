# gamification-tool
This is a web app based on Django with PostgreSQL for database and Docker for containarizing

Please make sure you installed Docker before running

# How to run
1. Spin up containers:  
`$ docker-compose up --build`

This builds and runs two containers:
1. web  
2. db  

Note: These containers can be referenced in terminal either by web and db, or by their id which can be found using `$ docker ps` to list currently running containers

Also note: Depending on the version of docker installation, the general terminal command could either be `$ docker-compose` or `$ docker compose`

## Access webpage

In browser: http://localhost:8000

We should have a hardcoded superuser in the database:
- username: admin, password: admin

If not, then make one using the following:  
`$ docker-compose exec web python manage.py createsuperuser`


_Note: this admin section will be removed from the readme once everyone's up and moving_

Admin endpoints can be reached at http://localhost:8000/admin/  
Similarly for each app in the project, e.g.: http://localhost:8000/check_in/

Currently API endpoints can be reached only for the user app:  
- http://localhost:8000/ returns the user API root  
- http://localhost:8000/users/ returns the list of users
- http://localhost:8000/users/\<id\>- returns the user by their id

More REST API endpoints will be added soon, and moved to the http://localhost:8000/api/v1/users




## Stop the container

1. To spin down a container:  
`$ docker-compose down`  
or CTRL+c

## Database migration
When updating models in Django, in order to update the database table for a specific app within the project, the following must be done:  
1. Create manifestation file:  
`$ docker-compose exec web python manage.py makemigrations \<app name\>`
2. Push database migration  
`$ docker-compose exec web python manage.py migrate`

If the migration isn't working due to a major change to a database table structure i.e. changing the user entity to a customised user entity, either drop the database and start with a fresh migration, or there are hack ways to comment out some auth sections in the code which will aloow the migration to go through you can find on stackoverflow.

## How to access database:

1. Open connection with postgresql:  
`$ docker-compose exec db psql -U <user> -d <database> --password`
2. Enter postgresql user password when prompted  

Once in:
- View databases: `\l`  
- Connect to database: `\c <database>` - (_should already be connected_)  
- Display tables: `\dt`   
- SQL queries, example: `SELECT * FROM auth_group;`

## How to open a python shell within the docker container:

1. Run bash inside the web container:  
`$docker-compose exec web sh`

2. Open python shell:  
`$python manage.py shell`  
- Or in a one liner:  
`$ docker-compose exec web python manage.py shell`

3. Import class and models from modules, save to db, etc.:
```
>>> from check_in.models import Location, Event
>>>from django.utils import timezone
>>> l = Location(location_name="Here", date_visited=timezone.now())
>>> l.save()
>>> l.id
```

## Testing
Unit tests are made in each app under tests.py

1. To run tests:  
`$ python manage.py test <app name>`

View testing requires using the python shell under test environment conditions. Look at Django tutorial part 5 in the documentation: [here](https://docs.djangoproject.com/en/5.1/intro/tutorial05/)


# Project applications
## 1. User: 
Custom user implementation built on top of Django users.
On top of the base implementation each user has:
- Total points
- Spendable points
- Level
- VIP user (a bool indicating a high contributor o Woofya)
- Avatar, which is either:
    - An uploaded image by the user
    - Or a cartoon representation of the user
- Lists of:
    - Dog entities
        - May contain their own avatar, cosmetics, etc.
    - Milestones (FK)
    - Titles (FK)
    - Badges (FK)
    - Any other cosmetics (FK)
    - locations visited (FK)
    - events visited (FK)

## 2. Check-in: 
Application for handling location and event check-ins.
Contains models for:
- Location
- Event

## 3. Leaderboard
Application for handling the user points leaderboard.

Depending on the implementations, leaderboard could be used for:
- Points accumulated over time
- Locations visited
- Measure related to their pets - e.g. distance walked, for example

## 4. Marketplace
Application for handling points-spending activities. Acts as not only the shop, but also the database to view all available items, purchaseable or not.

Contains:
- Shop
- Entities:
    - Badges
    - Titles
    - Milestones (_unsure if this should be here or in the user app_)
    - Any other cosmetics