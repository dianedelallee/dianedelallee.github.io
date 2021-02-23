---
title: How to use cache to install python lib with Gitlab CI
author: Diane Delallée
date: 2020-08-07 13:25:00 +0800
categories: [Blog, CI]
tags: [gitlab, ci, python]
---

If you have a CI process with multiple job that needs to install the same libraries, it can be very time consuming.
So you probably want to use a cache to not download each those libraries that you already have.

Lets start with a small ci file and we will see after how can we add configuration to tell gitlab to use the cache
## Small Example of gitlab-ci.yml file


```yaml
stages:
  - Initialization
  - QualityAndTest

"Init project":
  stage: Initialization
  image: <link to my docker container>
  script:
    - cd <path/to/the/project>
    - pip install -r requirements.txt

"Mypy":
  stage: QualityAndTest
  image: <link to my docker container>
  before_script:
    - cd <path/to/the/project>
    - pip install -r requirements.txt
    - pip install mypy
  script: 
    - cd <path to the source code>
    - mypy --config-file <myConfigFile> -p <package to check>

"Pylint":
  stage: QualityAndTest
  image: <link to my docker container>
  before_script:
    - cd <path/to/the/project>
    - pip install -r requirements.txt
    - pip install pylint
  script: 
    - cd <path to the source code>
    - pylint --rcfile <myConfigFile> <path to check>

"Test":
  stage: QualityAndTest
  image: <link to my docker container>
  before_script:
    - cd <path/to/the/project>
    - pip install -r requirements.txt
  script:
    - cd <path to my test>
    - pytest  # or coverage run ....
```

## How to use the cache

You need to add the `variables` and `cache` attribute at the top of the file. By defining a static key to the path
it will share the cache across branch and across pipeline.
```yaml
stages:
  - Initialization
  - QualityAndTest

# Change pip's cache directory to be inside the project directory since we can
# only cache local items.
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

# Pip's cache doesn't store the python packages
# https://pip.pypa.io/en/stable/reference/pip_install/#caching
#
# If you want to also cache the installed packages, you have to install
# them in a virtualenv and cache it as well.
cache:
  key: a-fixed-name
  paths:
    - .cache/pip
    - venv/

"Init project":
  stage: Initialization
  image: <link to my docker container>
  script:
    - cd <path/to/the/project>
    - pip install virtualenv
    - virtualenv venv
    - source venv/bin/activate
    - pip install -r requirements.txt

"Mypy":
  stage: QualityAndTest
  image: <link to my docker container>
  before_script:
    - cd <path/to/the/project>
    - pip install virtualenv
    - virtualenv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - pip install mypy
  script: 
    - cd <path to the source code>
    - mypy --config-file <myConfigFile> -p <package to check>

"Pylint":
  stage: QualityAndTest
  image: <link to my docker container>
  before_script:
    - cd <path/to/the/project>
    - pip install -r requirements.txt
    - pip install pylint
  script: 
    - cd <path to the source code>
    - pylint --rcfile <myConfigFile> <path to check>

"Test":
  stage: QualityAndTest
  image: <link to my docker container>
  before_script:
    - cd <path/to/the/project>
    - pip install virtualenv
    - virtualenv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
  script:
    - cd <path to my test>
    - pytest  # or coverage run ....
```

And that's all. Now each jobs is sharing the same cached and it should use it instead of downloading everything from Pypi.
### Useful links

You are new with gitlab-ci and need a default scripts.

For Python : [Python Ci File](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Python.gitlab-ci.yml)
For Django : [Django Ci File](https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Django.gitlab-ci.yml)

Looking for other language: 
[Check the templates](https://docs.gitlab.com/ee/ci/examples/#cicd-templates)
