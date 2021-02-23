---
title: Decorator and Structlog
author: Diane Delallée
date: 2020-12-08 10:18:00 +0800
categories: [Blog, Python]
tags: [logging, python]
---

During the Python web summit organized by [Geekle.us](https://geekle.us/), I listened to an interesting talk about Structlog library.
I decided to play a bit with it and with decorators, I implemented a small project about logging.

## Goal of the project
Create a decorator that will use structlog to add a logging system to each function of a class.

One of the goal is to have a trace_id to follow the code and to get easily information about the context when the function is called. 
For instance, the parameters provided to the function and the error message ...

## Different types of output

### Development
```shell
/home/dianedelallee/.local/share/virtualenvs/decoratorStructlog-eT6Dw5f0/bin/python /home/dianedelallee/Desktop/Diane/decoratorStructlog/main.py
2021-02-23T14:20:34.415087Z [info     ] Before calling the function    args=() function_name=models.Player.get_name kwargs={} trace_id=d3b9b48e-ce0e-4cc2-a48c-66cbfd6c0743
2021-02-23T14:20:34.415249Z [info     ] trying to get the name of the user trace_id=d3b9b48e-ce0e-4cc2-a48c-66cbfd6c0743
2021-02-23T14:20:34.415300Z [info     ] After calling the function     function_name=models.Player.get_name result=Diane trace_id=d3b9b48e-ce0e-4cc2-a48c-66cbfd6c0743
2021-02-23T14:20:34.415380Z [info     ] Before calling the function    args=() function_name=models.Player.get_age_in_cat_live kwargs={} trace_id=659685aa-4e90-4de5-bb22-44f32ac4fb57
2021-02-23T14:20:34.415418Z [info     ] trying to get the aage in cat referencial trace_id=659685aa-4e90-4de5-bb22-44f32ac4fb57
2021-02-23T14:20:34.415442Z [info     ] get cat referential            trace_id=659685aa-4e90-4de5-bb22-44f32ac4fb57
2021-02-23T14:20:34.415461Z [info     ] After calling the function     function_name=models.Player.get_age_in_cat_live result=210 trace_id=659685aa-4e90-4de5-bb22-44f32ac4fb57

Process finished with exit code 0

```
### Production
```shell
/home/dianedelallee/.local/share/virtualenvs/decoratorStructlog-eT6Dw5f0/bin/python /home/dianedelallee/Desktop/Diane/decoratorStructlog/main.py
{
  "args": [],
  "event": "Before calling the function",
  "function_name": "models.Player.get_name",
  "kwargs": {},
  "level": "info",
  "timestamp": "2021-02-23T14:21:41.464028Z",
  "trace_id": "8fdbd416-d109-4671-8b57-cc28a9ebbbe6"
}
{
  "event": "trying to get the name of the user",
  "level": "info",
  "timestamp": "2021-02-23T14:21:41.464145Z",
  "trace_id": "8fdbd416-d109-4671-8b57-cc28a9ebbbe6"
}
{
  "event": "After calling the function",
  "function_name": "models.Player.get_name",
  "level": "info",
  "result": "Diane",
  "timestamp": "2021-02-23T14:21:41.464183Z",
  "trace_id": "8fdbd416-d109-4671-8b57-cc28a9ebbbe6"
}
{
  "args": [],
  "event": "Before calling the function",
  "function_name": "models.Player.get_age_in_cat_live",
  "kwargs": {},
  "level": "info",
  "timestamp": "2021-02-23T14:21:41.464245Z",
  "trace_id": "1f18db5d-c8dc-4886-8639-2a3baf96ce45"
}
{
  "event": "trying to get the aage in cat referencial",
  "level": "info",
  "timestamp": "2021-02-23T14:21:41.464285Z",
  "trace_id": "1f18db5d-c8dc-4886-8639-2a3baf96ce45"
}
{
  "event": "get cat referential",
  "level": "info",
  "timestamp": "2021-02-23T14:21:41.464313Z",
  "trace_id": "1f18db5d-c8dc-4886-8639-2a3baf96ce45"
}
{
  "event": "After calling the function",
  "function_name": "models.Player.get_age_in_cat_live",
  "level": "info",
  "result": 210,
  "timestamp": "2021-02-23T14:21:41.464336Z",
  "trace_id": "1f18db5d-c8dc-4886-8639-2a3baf96ce45"
}

Process finished with exit code 0
```

## References
* [Struct log library](https://www.structlog.org/en/20.1.0/index.html)
* [Nice Article about struclog](https://atymo.me/blog/python_logging.html)

## Full project 
In [this Github repo](https://github.com/dianedelallee/decoratorStructlog) 
