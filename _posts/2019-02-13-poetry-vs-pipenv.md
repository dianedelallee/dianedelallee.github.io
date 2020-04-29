---
title: Poetry instead of Pipenv?
author: Diane Delallée
date: 2019-02-13 20:55:00 +0800
categories: [Blog, Configuration]
tags: [pipenv, poetry]
---

One month ago I wrote about Pipenv because I appreciate how it is easy to set up a virtual env and because I have to use at work.

Today, I have discovered [Poetry](https://python-poetry.org/), and decide to play a bit with

First, I create a folder, go to it and install Poetry

```shell
mkdir poetry_test
cd poetry_test
pip3 install poetry
```

Lets create our new python project

```shell
poetry new package_project
cd package_project
ls

package_project
├── pyproject.toml
├── README.rst
├── package_project
│   └── __init__.py
└── tests
    ├── __init__.py
    └── test_package_project.py
```

In the pyproject.toml, you will find everything you need about your dependency and specification about your project.
pyproject.toml is the Minimum Build System Requirements for Python Projects ([PEP 518](https://www.python.org/dev/peps/pep-0518/)). In other words, poetry uses pyproject.toml to replace setup.py, requirements.txt, setup.cfg, MANIFEST.in and the newly added Pipfile.

If you need to install a new library, just type

```shell
poetry add requests
Creating virtualenv package-project-py3.6 in /Users/ddelalle/Library/Caches/pypoetry/virtualenvs
Using version ^2.21 for requests

Updating dependencies
Resolving dependencies... (0.4s)


Package operations: 12 installs, 0 updates, 0 removals

Writing lock file

  - Installing six (1.12.0)
  - Installing atomicwrites (1.2.1)
  - Installing attrs (18.2.0)
  - Installing certifi (2018.11.29)
  - Installing chardet (3.0.4)
  - Installing idna (2.8)
  - Installing more-itertools (5.0.0)
  - Installing pluggy (0.8.1)
  - Installing py (1.7.0)
  - Installing urllib3 (1.24.1)
  - Installing pytest (3.10.1)
  - Installing requests (2.21.0)
```

If you need to activate your virtual env

`poetry shell`

Add a main file touch package_project/main.py and, you are now ready to start working.
My package is finished, I want to publish it
After a lot of hours of code, you wnat now to build and publish your code on Pypi? Really easy, just write

```shell
poetry build
poetry publish
```

You will fin all the commands and documentation [here](https://python-poetry.org/docs/cli/)
