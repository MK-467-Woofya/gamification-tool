# gamification-tool
This is a web app based on Django with PostgreSQL for database and Docker for containarizing

please make sure you installed Docker before running

# how to run

docker-compose up --build

# database migration

docker-compose exec web python manage.py migrate

# access webpage

http://localhost:8000

# stop the container

docker-compose down

