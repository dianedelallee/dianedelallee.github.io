---
title: Block website to improve focuses
author: Diane Delallée
date: 2021-02-25 09:44:00 +0800
categories: [Blog, Python]
tags: [python, cron, focus]
---

As I am now fully working from home, break and hot beverage breaks are totally different. No more breaks where you can talk with 
colleagues, no more "forced" break to eat croissants 🥐. I am not really good to take a real break for few minutes not in front of my computer.

Usually, I go to some websites like twitter or Linkedin to check some news, but it can be unmanageable. To help me focus, I have decided
at the beginning of the year, to put several actions in place.

## Block some websites during working hours.
Those website did not provide me a lot of useful information, so I have decided to block them during working hours, and If needed I
can still check them after those hours. This helps me a lot to stay focuses on my work.

here is the code to do so: 

<script src="https://gist.github.com/dianedelallee/93472ae62fde8288606c1c2a6ed35ffb.js"></script>

My computer for work is under Ubuntu, so this is how I run automatically this file.
In your terminal
```shell
crontab -e
```

It will open the file and I have only added this line

```
45 7 * * MON-FRI /usr/bin/python3 ~/desktop/python_website_blocker.py >> ~/cron.log 2>&1
```

It means that each morning at 7:45AM my ypthon file which is called `python_website_blocker.py` will be execute.


## Still need/want to read technical articles
Really easily, I selected some interesting authors, or blog, take their RSS feed link and use [Feedly](https://feedly.com/)
to read all my articles without any distractions.

I am really happy with those decisions, and feeling really less guilty at the end of some days!
