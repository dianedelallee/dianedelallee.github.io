---
title: Launch a Django app in a Docker and be ready to put in Production
author: Diane Delallée
date: 2020-01-15 20:55:00 +0800
categories: [Blog, Python]
tags: [Docker, Python, Django]
---

New year, new resolution, so today I have decided to play a bit with Docker, Django, Gunicorn and Nginx. So first we will create a Django in a Docker with a Postgres DB, and after we will add production environment and Nginx and Gunicorn. lets create the project

## Lets create a Django project

```shell
mkdir django-in-a-docker && cd django-in-a-docker
mkdir app && cd app
python3.7 -m venv env
source env/bin/activate
(env)$ pip install django==2.2.9
(env)$ django-admin.py startproject hello_django .
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

if you navigate to [http://localhost:8000/](http://localhost:8000/) you should see the Django welcome screen.
In order to put all our libraries in the same file, we will create a requirements.txt file which contains `Django==2.2.9`
As we will use Postgres, we can remove the db.sqlite file from the "app" directory. Now your Django project works, let continue a create the Docker files.

## Start to play with Docker

Now your project directory should look like that:

```shell
django-in-a-docker
|\_ app
├── hello_django
│ ├── **init**.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── manage.py
└── requirements.txt
```

If you do not have Docker install please [install Docker](https://docs.docker.com/get-docker/). Then you create a Dockerfile to the app directory. And write the following configuration in it

```python
# pull official base image
FROM python:3.7.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
```

We are using an Alpine version of Docker for Python 3.7, and we set the working directory. We also update pip and install all the requirements.

Now we will need to define the docker-compose.yml file. Place it in the "django-in-a-docker" directory (same level as the app directeory) and write that

```python
version: '3.7'

services:
web:
build: ./app
command: python manage.py runserver 0.0.0.0:8000
volumes: - ./app/:/usr/src/app/
ports: - 8000:8000
env_file: - ./.env.dev
```

Now we will update the SECRET_KEY, DEBUG and ALLOWED_HOSTS in settings.py to place them in a .env.dev file. This file should be in the "django-in-a-docker" directory.
In your settings.py changeyour code by that:

```python
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(", ")
```

and in the .env.dev

```
DEBUG=1
SECRET_KEY=my_anazing_secret_key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

## Lets configure our Postgres DB

To configure Postgres, we'll need to add a new service to the docker-compose.yml file, update the Django settings, and install Psycopg2. Lets update the docker-compose.yml

```python
version: '3.7'

services:
web:
build: ./app
command: python manage.py runserver 0.0.0.0:8000
volumes: - ./app/:/usr/src/app/
ports: - 8000:8000
env_file: - ./.env.dev
depends_on: - db
db:
image: postgres:12.0-alpine
volumes: - postgres_data:/var/lib/postgresql/data/
environment: - POSTGRES_USER=hello_django - POSTGRES_PASSWORD=hello_django - POSTGRES_DB=hello_django_dev

volumes:
postgres_data:
```

We can also update the .env.dev file

```python
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
```

In the settings.py we now need to update the DATABASES section. Replace it by

```python
DATABASES = {
    "default": {
    "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
    "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
    "USER": os.environ.get("SQL_USER", "user"),
    "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
    "HOST": os.environ.get("SQL_HOST", "localhost"),
    "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}
```

Lets update the Dockerfile to install Psycopg2

```python
# pull official base image
FROM python:3.7.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
```

And last step, we will need to add Psycopg2 to our requirements.txt

```
Django==2.2.9
psycopg2-binary==2.8.3
```

We have to build our docker and run the migrations

```shell
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate --noinput
```

To be sure that the django table are properly created, just run

```shell
docker-compose exec db psql --username=hello_django --dbname=hello_django_dev

psql (12.0)
Type "help" for help.

hello_django_dev=# \l
List of databases
Name | Owner | Encoding | Collate | Ctype | Access privileges
------------------+--------------+----------+------------+------------+-------------------------------
hello_django_dev | hello_django | UTF8 | en_US.utf8 | en_US.utf8 |
postgres | hello_django | UTF8 | en_US.utf8 | en_US.utf8 |
template0 | hello_django | UTF8 | en_US.utf8 | en_US.utf8 | =c/hello_django +
| | | | | hello_django=CTc/hello_django
template1 | hello_django | UTF8 | en_US.utf8 | en_US.utf8 | =c/hello_django +
| | | | | hello_django=CTc/hello_django
(4 rows)

hello_django_dev=# \c hello_django_dev
You are now connected to database "hello_django_dev" as user "hello_django".

hello_django_dev=# \dt
List of relations
Schema | Name | Type | Owner
--------+----------------------------+-------+--------------
public | auth_group | table | hello_django
public | auth_group_permissions | table | hello_django
public | auth_permission | table | hello_django
public | auth_user | table | hello_django
public | auth_user_groups | table | hello_django
public | auth_user_user_permissions | table | hello_django
public | django_admin_log | table | hello_django
public | django_content_type | table | hello_django
public | django_migrations | table | hello_django
public | django_session | table | hello_django
(10 rows)

hello_django_dev=# \q
```

## Define entrypoint.sh

To check if the Postgres DB is healthy we will add a entrypoint.sh. It will helps us to not run migrations on unhealthy DB. Create this file in te "app" folder and copy/paste those lines.

```sh
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"

fi

python manage.py flush --no-input
python manage.py migrate

exec "\$@"
```

you now need to change the permissions on the file by `chmod +x app/entrypoint.sh`. Now we can update the Dockerfile to copy over the entrypoint.sh

```python
# pull official base image
FROM python:3.7.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
```

We will add the DB to the env.dev file

```
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

Okay so lets rebuild our docker image and run the container

```shell
docker-compose up -d --build
```

If you navigate to [http://localhost:8000/](http://localhost:8000/) you should see again the Django Welcome page :-). Well done, your Django in a Docker works perfectly for development environment

## Lets configure it to be ready for Production

### Gunicorn

In our requirements.txt, lets add the Gunicorn reference

```
Django==2.2.9
gunicorn==19.9.0
psycopg2-binary==2.8.3
```

Since we still want to use Django's built-in server in development, create a new compose file called docker-compose.prod.yml for production

```
version: '3.7'

services:
web:
build:
context: ./app
dockerfile: Dockerfile.prod
command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
ports: - 8000:8000
env_file: - ./.env.prod
depends_on: - db
db:
image: postgres:12.0-alpine
volumes: - postgres_data:/var/lib/postgresql/data/
env_file: - ./.env.prod.db

volumes:
postgres_data:
```

As you can see in the docker-compose.prod.yml we have define a .env.prod and a .env.prod.db files to store all the varaible relative to the production. Lets create this file in the "django-in-a-docker" directory and write that

```
# .env.prod

DEBUG=0
SECRET_KEY=change_me
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_prod
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

```
# .env.prod.db

POSTGRES_USER=hello_django
POSTGRES_PASSWORD=hello_django
POSTGRES_DB=hello_django_prod
```

Lets create the Production Docker file now. First we need to create our entrypoint.prod.sh and as previously update the permissions on it `chmod +x app/entrypoint.prod.sh`

```sh
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"

fi

exec "\$@"
```

To use this file, create a new Dockerfile called Dockerfile.prod for use with production builds

```python
###########
# BUILDER
###########

# pull official base image
FROM python:3.7.0-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL
#########

# pull official base image
FROM python:3.7.0-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/\*

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh \$APP_HOME

# copy project
COPY . \$APP_HOME

# chown all the files to the app user
RUN chown -R app:app \$APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]
```

### Nginx

We need to add this service to our docker-compose.proc.yml

```
version: '3.7'

services:
web:
build:
context: ./app
dockerfile: Dockerfile.prod
command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
ports: - 8000:8000
env_file: - ./.env.prod
depends_on: - db
db:
image: postgres:12.0-alpine
volumes: - postgres_data:/var/lib/postgresql/data/
env_file: - ./.env.prod.db
nginx:
build: ./nginx
ports: - 1337:80
depends_on: - web

volumes:
postgres_data:
```

Lets create in the django-in-a-docker directory a new folder called "nginx" which will contains two files. one Dockerfile and one nginx.conf

```python
# Dockerfile

FROM nginx:1.17.4-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

```python
# nginx.conf:
upstream hello_django {
server web:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://hello_django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

now we need to update our docker-compose.prod.yml to take this change into account

```
version: '3.7'

services:
web:
build:
context: ./app
dockerfile: Dockerfile.prod
command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
expose: - 8000
env_file: - ./.env.prod
depends_on: - db
db:
image: postgres:12.0-alpine
volumes: - postgres_data:/var/lib/postgresql/data/
env_file: - ./.env.prod.db
nginx:
build: ./nginx
ports: - 1337:80
depends_on: - web

volumes:
postgres_data:
```

Now our app should be like that

```shell
├── .env.dev
├── .env.prod
├── .env.prod.db
├── .gitignore
├── app
│ ├── Dockerfile
│ ├── Dockerfile.prod
│ ├── entrypoint.prod.sh
│ ├── entrypoint.sh
│ ├── hello_django
│ │ ├── **init**.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ └── wsgi.py
│ ├── manage.py
│ └── requirements.txt
├── docker-compose.prod.yml
├── docker-compose.yml
└── nginx
├── Dockerfile
└── nginx.conf
```

## Static files

### How to configure the development environment

Lets update the settings.py

```python
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
```

We can now update the entrypoint.sh in order to collect all the static files

```sh
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"

fi

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "\$@"
```

### How to configure the production environment

For production, add a volume to the web and nginx services in docker-compose.prod.yml so that each container will share a directory named "staticfiles":

```
version: '3.7'

services:
web:
build:
context: ./app
dockerfile: Dockerfile.prod
command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
volumes: - static_volume:/home/app/web/staticfiles
expose: - 8000
env_file: - ./.env.prod
depends_on: - db
db:
image: postgres:12.0-alpine
volumes: - postgres_data:/var/lib/postgresql/data/
env_file: - ./.env.prod.db
nginx:
build: ./nginx
volumes: - static_volume:/home/app/web/staticfiles
ports: - 1337:80
depends_on: - web

volumes:
postgres_data:
static_volume:
```

We need to also create the "/home/app/web/staticfiles" folder in Dockerfile.prod:

```python
...

# create the appropriate directories

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR \$APP_HOME

...
```

Now we have to update our Nginx configuration to route static file requests to the staticfiles folder

```
upstream hello_django {
server web:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://hello_django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    location /staticfiles/ {
        alias /home/app/web/staticfiles/;
    }
}
```

Now lets try our code in the production environment

```shell
docker-compose down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

Now if you go to [http://localhost:1337/admin](http://localhost:1337/admin) you should css the proper Django admin login page with the default django css apply. Well done you have finished the configuration of your Django application.

You will be able to find the code [here](https://github.com/dianedelallee/django-in-a-docker)

## References

- **Alpine-base Docker image:** [Docker-Alpine](https://github.com/gliderlabs/docker-alpine)
- **Docker Working Directory:** [WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir)
- **Docker for Python Developers:** [slides - help you to construct your DockerFiles](https://mherman.org/presentations/dockercon-2018/#1)
- **Gunicorn:** [doc](https://gunicorn.org/)
- **Nginx:** [doc](https://www.nginx.com/resources/glossary/reverse-proxy-server/)
