---
title: Json in command line
author: Diane Delallée
date: 2019-03-17 20:55:00 +0800
categories: [Blog, Configuration]
tags: [json]
---

When I am debugging a part of a code which does not work, I print quite often some dictionary of a json object in my shell.
Most of the time it happens in one line quite difficult to read, so I open bracket and format my JSON to have better readability.

Recently I discover [jq](https://stedolan.github.io/jq/), which can manage to print your JSON file in your terminal. I will save a lot of time.

```shell
echo '{"foo": 123, "bar": "abc"}' | jq
{
  "foo": 123,
  "bar": "abc"
}
```

I want to access an attribute of my JSON I only need to write

```shell
echo '{"foo": 123, "bar": "abc"}' | jq '.bar'
"abc"
```

You can also mix `curl` and `jq` if you want to display beautifully the result of an API in your terminal.

```shell
curl https://api.github.com/repos/dianedelallee/python-exercise |jq
{
  "id": 144120613,
  "node_id": "MDEwOlJlcG9zaXRvcnkxNDQxMjA2MTM=",
  "name": "python-exercise",
  "full_name": "dianedelallee/python-exercise",
  "private": false,
   ...
   ...
  "default_branch": "master",
  "network_count": 0,
  "subscribers_count": 1
}
```
