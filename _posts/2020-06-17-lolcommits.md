---
title: Lolcommits
author: Diane Delallée
date: 2020-06-17 16:25:00 +0800
categories: [Blog, commit]
tags: [github, fun]
---

Few months ago, I discovered this really funny repo: [lolcommits](https://lolcommits.github.io/).
It will take a picture of you each time you are making a commit. This is really fun to see how your evolution accross month.

## How to use it
```bash
brew install imagemagick
sudo gem install lolcommits
cd path/to/the/git/repo/where/you/want/to/take/pictures
lolcommits --enable --delay 3 --fork
```

If you want to disabled it 
```bash
lolcommits --disable
```

It will save all your photo in the repo `cd ~/.lolcommits`, so you can easily see them.

If you want to generate a nice gif with all your photo you can use the command
`lolcommits --timelapse` but you can not define the duration of the gif.

I prefer to use `convert -delay 20 -loop 0 *.jpg myimage.gif` to generate my commit-gif !

here is the final result


![lol-commit.gif]({{ site.baseurl }}/img/lol_commit.gif)
