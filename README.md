
## Prerequisites

* Docker `docker`
* Docker compose `docker-compose`

## Django bootstrap actions

Make migrations:
```bash
docker-compose run --rm django_app python manage.py makemigrations
docker-compose run --rm django_app python manage.py migrate
```

Create admin user:
```bash
docker-compose run --rm django_app python manage.py createsuperuser
```

# Using your application

Start your application by running:
```bash
docker-compose up --build
```
