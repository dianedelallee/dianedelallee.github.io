---
title: How to easily import data from CSV file in Django
author: Diane Delallée
date: 2019-11-22 20:55:00 +0800
categories: [Blog, Python]
tags: [django, csv]
---

I need to import a lot of data but I do not want to do that manually. How can I take a CSV file and import it in my Django table?

I will show you how I use the `django-import-export` library to do that. Let's say I have a model called event which has a foreign key to link an event to a user.

First you need to install the library and declare it in my INSTALLED_APPS by adding 'import_export'
in the models.py

```python
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.TextField()
    user_ref = models.ForeignKey(User, models.PROTECT)
```

I would like know to import a csv which contains only the name, the date and the location. To do that lets create a view which take in parameters the user id
in the urls.py

```python
from django.urls import re_path
urlpatterns = [
    re_path(r'^user/(?P\d+)/event/create_bunch$', my_view.create_bunch_events_for_user,
                name="create-events-for-user"),
]
```

in the my_view.py

```python
import tablib
from import_export import resources
from models import Event

def create_bunch_events_for_user(request, user_id):
    if request.method == 'POST':
        event_resource = resources.modelresource_factory(model=Event)() # to take the model as a reference
        new_events = request.FILES['csv_events'] # to get the file
        # this part is to add the a column with the user id
        dataset = tablib.Dataset(
            headers=['name', 'date', 'location']
        ).load(new_events.read().decode('utf-8'), format='csv')
        dataset.append_col(
            col=tuple(f'{user_id}' for _ in range(dataset.height)),
            header='user_id'
        )
        result = event_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            event_resource.import_data(dataset, dry_run=False)  # Actually import now

    return redirect(reverse('create-events-for-user', args=(user_id,)))
```

and finally in your html file

<img src="https://www.fatalement.com/static/img/import-csv-html.png" width="100">

The view which use this html file as template should provide the user in the context.

Your csv file should seems like that:

```
name,date,location
Event 1,2019-02-22,Paris
Event 2,2019-08-01,Lausanne
```

And that is it, now you should see the data who are in your csv in your database.

I hope it will help you. Feel free to write me a message if you have questions about this article
