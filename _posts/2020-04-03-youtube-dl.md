---
title: My favourite and most useful alias
author: Diane Delallée
date: 2020-04-03 20:55:00 +0800
categories: [Blog, Configuration]
tags: [configuration, alias]
---

A few years ago, I discovered this really nice library called [youtube-dl](https://github.com/ytdl-org/youtube-dl). This library allows you to download video from youtube and other platforms.
Here is my alias to only download the mp3 and put it in a specific folder

```shell
alias getmusic='function _music(){ cd ~/Desktop/Music/Download; youtube-dl -o "%(title)s.%(ext)s" -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" -x --audio-format mp3 --no-mtime --prefer-ffmpeg $1; cd -;};_music'
```

Small explanation on what this function does.
First, it goes to my Music/Download folder.
Then -o will define the name of my file -> in this case I want the name of youtube video and the extension. It will give me "Amazing_song.mp3"
-f is for the format -> so in that case, we download the video in mp4 format with the best video and audio resolution
-x will extract the audio
--audio-format will specify the format of the audio we just extract
--no-mtime means we do not copy the mtime
--prefer-ffmpeg means we prefer ffmpeg over avconv for running the postprocessors (default)

at the end of the process the mp4 file will be automaticall deleted and
with cd - we only return to the folder we where at the begining
If you provide the url of a playlist it will doanload you the full playlist.
to run this alias just do:

```
getmusic https://www.youtube.com/watch\?v\=TB_eVIS8JQs
```

And if you want to download a music from soundcloud, it is even easier !

```
alias getsound='function _sound(){ cd ~/Desktop/Music/Download; youtube-dl $1;cd -;};_sound'
```

And only call your new alias

```
getsound https://soundcloud.com/buvette/the-maze
```

And that is it. You can now enjoy your MP3! But of course, if you enjoy the band, do not forget to buy them some CD, vinyl, or go to see them in concert to help them !
