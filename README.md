# Gymkhana Portal ![Status active](https://img.shields.io/badge/Status-active%20development-2eb3c1.svg) ![Django 2.1.5](https://img.shields.io/badge/Django-2.1.5-green.svg) ![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg)

[![Build Status](https://travis-ci.org/devlup-labs/gymkhana_portal.svg?branch=master)](https://travis-ci.org/devlup-labs/gymkhana_portal)

## Web portal and forum for Students' Gymkhana of IIT Jodhpur created by Saurabh Kumar

### Purpose

Simplify the workflow of updating the gymkhana website without much knowledge on how to code. And also provide certain utility features.

This project includes:

- A main `web portal` which can be updated dynamically through an admin interface.
- A `forum/discussion` app for general purpose discussions.
- An app called `Konnekt` to find/search people with a certain required skill set.

### Installation:

Requirements:

- Python 3.6 runtime
- Django >= 2.1.6
- Other dependencies in `Pipfile`

Procedure:

- Install [python](https://www.python.org/downloads/) in your environment(pre-installed on Ubuntu).

- Navigate to the cloned repository.

```sh
cd <project_directory_name>     # gymkhana_portal
```

- Install `pipenv` for dependency management

```sh
pip install pipenv
```

- Copy `.env.example` to `.env`

```sh
cp .env.example .env
```

- Use pipenv to install other dependencies from `Pipfile`

```sh
pipenv install --dev
```

- Activate the new virtual environment

```sh
pipenv shell
```

- Change to source code directory

```text
cd src
```

- Make database migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

- Create a superuser

```sh
python manage.py createsuperuser
```

- Download the `static.zip` from `#gymkhana` on [Slack](https://iitjdg.slack.com/) and extract the contents under `src/static`  
   *Note: This project uses proprietary UI assets, which cannot be shared on GitHub. However you may use free version of [mdbootstrap](https://mdbootstrap.com) as an alternative. Some things may not look as intended.*

- Run development server on localhost

```sh
python manage.py runserver 
```

#### DummyData for Testing [OPTIONAL]:

This will populate the database with random values for testing.

```sh
python manage.py createfixture 
```
