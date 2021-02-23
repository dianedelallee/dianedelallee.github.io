---
title: NamedTuple
author: Diane Delallée
date: 2019-01-28 20:55:00 +0800
categories: [Blog, Python]
tags: [Python]
---

Thanks to an amazing tweet of [Sam & Max](http://sametmax.com/), I have read an article about how to start with Python in 2019 which give me the opportunity to watch the video [Beyond PEP8](https://www.youtube.com/watch?v=wf-BqAjZb8M) from Raymond Hettinger.

This is how I discover and understand how to use the NamedTuple

Before

```python
p = (120, 50, 100)
if p[0] > 100:
    print('do something')
if p[1] <= 50:
    print('do something else')
```

This is how it works with namedtuple

```python
from collections import namedtuple

color = namedtuple('color', ['hue', 'saturation', 'luminosity'])

p = color(170, 20, 50)
if p.hue > 100:
    print('do something')
if p.saturation <= 50:
    print('do something else')
```

you should use named tuples instead of tuples anywhere you think object notation will make your code more pythonic and more easily readable.

If you need more details or/and advance tips: [PSF documentation](https://docs.python.org/3/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields)
