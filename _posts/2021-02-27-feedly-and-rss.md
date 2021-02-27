---
title: Feedly and RSS flux for this website
author: Diane Delallée
date: 2021-02-27 11:36:00 +0800
categories: [Blog, RSS]
tags: [rss]
---

Few weeks ago, I decided to adopt new behaviour for 2021 (another article will come soon). One of those new behaviour is
to stop infinite scroll on some websites like twitter.

But how to get notify about interesting articles?


Using [Feedly](https://feedly.com/) to load some RSS flux that I want to follow, and that's it. 
Only articles that are relevant are shown in this app, and when I want to take a break, I can read them from feedly without
be tempted to navigate and loose myself in the web.

## Reading RSS now, but how this website generate RSS about my articles.

This [Jekyll theme](https://github.com/cotes2020/jekyll-theme-chirpy) already provide a RSS system.
The code that generate the RSS flux is in the [feed.xml file](https://github.com/dianedelallee/dianedelallee.github.io/blob/master/feed_old.xml).

I was not very happy with the RSS flux provided by the theme, cause it truncate the content to 200 characters (cf [line 53](https://github.com/dianedelallee/dianedelallee.github.io/blob/master/feed_old.xml#L53)).

I try to remove this truncate, but I was still not very pleased with the result. To not loose this RSS generator, I renamed the file to `feed_old.xml` and instead I use another xml template to generate my RSS flux.
You can find it [here](https://github.com/dianedelallee/dianedelallee.github.io/blob/master/feed_old.xml).

You can see the result of my RSS flux in [https://fatalement.com/feed.xml](https://fatalement.com/feed.xml) and it looks like that in me feedly app:

<img src="https://fatalement.com/assets/img/sample/feedly_fatalement.png" alt="Feedly rss flux"/>

and this is how an article looks like when you read it

<img src="https://fatalement.com/assets/img/sample/feedly_article.png" alt="Feedly show article"/>
