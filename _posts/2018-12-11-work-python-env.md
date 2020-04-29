---
title: Work in a proper python environment
author: Diane Delallée
date: 2018-12-11 20:55:00 +0800
categories: [Blog, Python]
tags: [Python, Configuration]
---

When you start a new python project, it is quite important to have a proper environment.
With Pipenv, it is quite easy to create a virtual environment, install libraries and manage the version of those libraries.

As I am using Brew, it is easy to install and to use.
Let's see that.

## Installation

`brew install pipenv`

## New project and Pipenv workflow

My new project is in ~/Desktop/development/my_project

`cd ~/Desktop/development/my_project`

I want to create my Pipfile (to know which libraries are installed with which a specific version).

Let's call Pipenv to install the requests library.

`pipenv install requests`

you should see

```shell
Creating a virtualenv for this project…
Pipfile: ~/Desktop/development/my_project/Pipfile
Using /usr/local/Cellar/pipenv/2018.11.26/libexec/bin/python3.7 (3.7.1) to create virtualenv…
⠇ Creating virtual environment...Already using interpreter /usr/local/Cellar/pipenv/2018.11.26/libexec/bin/python3.7
Using real prefix '/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7'
New python executable in /Users/ddelalle/.local/share/virtualenvs/dev_test_example-5dI9ifch/bin/python3.7
Also creating executable in /Users/ddelalle/.local/share/virtualenvs/dev_test_example-5dI9ifch/bin/python
Installing setuptools, pip, wheel...
done.

✔ Successfully created virtual environment!
Virtualenv location: /Users/ddelalle/.local/share/virtualenvs/my_project-5dI9ifch
Creating a Pipfile for this project…
Installing requests…
Adding requests to Pipfile's [packages]…
✔ Installation Succeeded
Pipfile.lock not found, creating…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
✔ Success!
Updated Pipfile.lock (444a6d)!
Installing dependencies from Pipfile.lock (444a6d)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 5/5 — 00:00:03
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

If you check you will now have a Pipfile in your repository.
Now, I want to run my virtual env and start to work on my project.

`pipenv shell`

you should see

```shell
Launching subshell in virtual environment…
 . /Users/ddelalle/.local/share/virtualenvs/my_project-5dI9ifch/bin/activate
```

That is it! You now have a proper environment to work.
If you need to exit your virtual env, just write

`exit`

You can find more explanation and more configuration in the [Pipenv project page](https://pipenv.pypa.io/en/latest/basics/).
