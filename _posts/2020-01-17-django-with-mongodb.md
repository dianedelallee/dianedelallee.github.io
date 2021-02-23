---
title: Use MongoDB with Django
author: Diane Delallée
date: 2020-01-17 20:55:00 +0800
categories: [Blog, Python]
tags: [python, mongoDB, django]
---

We will try to use MongoDB with a Django project. To do that we will use the library called [Djongo](https://github.com/nesdis/djongo). I have take the previous project ([Django-in-a-docker]({% post_url 2020-01-15-django-in-a-docker %})) and I have removed all files relative to the production environment. I have built and run my container to check that everything works as expected. I have finally created a Super User to access the DB.

```
docker-compose up -d --build
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
```

First, we will need to add Djongo to our requirements.txt and rebuild our docker image. We also need to specify the version for sqlparse because Django is expected a special one.

```python
#requirements.txt
sqlparse==0.2.4
Django==2.2.9
djongo==1.3.0
```

Once it is done, lets change on docker-compose.yml to reference the mongoDB

```yml
version: '3.7'

services:
web:
build: ./app
command: python manage.py runserver 0.0.0.0:8000
volumes: - ./app/:/usr/src/app/
ports: - 8000:8000
env_file: - ./.env.dev
depends_on: - mongodb
mongodb:
image: mongo
volumes: - ./data-db:/data/db
ports: - 27017:27017

volumes:
postgres_data:
```

Once it is done, we can change in settings.py our database config and update the fields also in .env.dev

```python
#settings.py

DATABASES = {
    'default': {
    'ENGINE': os.environ.get("NOSQL_ENGINE", "djongo"),
    'NAME': os.environ.get("NOSQL_NAME", "test"),
    'HOST': os.environ.get("NOSQL_HOST", "mongodb"),
    'ENFORCE_SCHEMA': os.environ.get("NOSQL_ENFORCE_SCHEMA", True)
    }
}
```

```python
#.env.dev
DEBUG=1
SECRET_KEY=svmv+s(fwlwzxq7d7kmiu_m9^hvu\$^wi5q34zh5_s2=khsqpcv
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] 0.0.0.0
NOSQL_ENGINE=djongo
NOSQL_NAME=test
NOSQL_HOST=mongodb
NOSQL_ENFORCE_SCHEMA=False
```

Perfect, now we will create a model called Article which for now will only contains a title. Tihis model soulh be into my_website/models.py

```python
from django.db import models

class Article(models.Model):
title = models.TextField()
```

In to the directory my_website lets create a admin.py file and paste the following code

```python
from django.contrib import admin
from.models import Article

class ArticleAdmin(admin.ModelAdmin):
list_display = ['id', 'title']
list_display_links = ['id', ]
search_fields = ['title']

admin.site.register(Article, ArticleAdmin)
```

You can now rebuild the docker image and run the migrations, and create a superuser

```shell
docker-compose up -d --build
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --fake-initial
docker-compose exec web python manage.py migrate createsuperuser
```

If you try to reach the [webserver](http://0.0.0.0:8000/admin), you should be able to log in and see your Article model. If you try to create one, you can only define the title. If you go back to the Article model file, you can now add other attributes, like those ones for instance

```python
from django.db import models

class Article(models.Model):
title = models.TextField()
Author = models.TextField(default=None, blank=True)
tag = models.CharField(default=None, blank=True, max_length=255)
```

Just go back to the admin page and reload it. You should, without applying any migrations, see our new fields. It means that your MongoDB is properly defined and you can modify your model as you want.

you will be able to find the project [here](https://github.com/dianedelallee/django-with-mongodb)
