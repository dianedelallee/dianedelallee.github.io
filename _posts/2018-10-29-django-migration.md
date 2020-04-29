---
title: Django migrations
author: Diane Delallée
date: 2018-10-29 14:10:00 +0800
categories: [Blog, Python]
tags: [Python, Django]
---

How create a named empty migration in a specific django app?

`./manage.py makemigrations --empty my_django_app_name -n name_of_my_migration`

How run some python code in my migration?

```python
from django.db import migrations

def my_function_with_my_python_code(apps, schema_editor):
    print('write your python code here')


class Migration(migrations.Migration):

    dependencies = [
        ('django_app_name', 'name_of_migration_dependencies'),
    ]

    operations = [
        migrations.RunPython(my_function_with_my_python_code),
    ]
```

How to call some Django model in my migration?

```python
from django.db import migrations

def my_function_with_my_python_code(apps, schema_editor):
    MyModel = apps.get_model('django_app_name', 'MyModel')
    res = MyModel.objects.all()
    print('write your python code here')


class Migration(migrations.Migration):

    dependencies = [
        ('django_app_name', 'name_of_migration_dependencies'),
    ]

    operations = [
        migrations.RunPython(my_function_with_my_python_code),
    ]
```
