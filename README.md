# Gymkhana Portal ![Status active](https://img.shields.io/badge/Status-active%20development-2eb3c1.svg) ![Django 2.0.4](https://img.shields.io/badge/Django-2.0.4-green.svg) ![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg)
[![Build Status](https://travis-ci.org/devlup-labs/gymkhana_portal.svg?branch=master)](https://travis-ci.org/devlup-labs/gymkhana_portal)
## Web portal and forum for Students' Gymkhana of IIT Jodhpur
### Purpose
Simplify the workflow of updating the gymkhana website without much knowledge on how to code. And also provide certain utility features.

This project includes:
- A main `web portal` which can be updated dynamically through an admin interface.
- A `forum/discussion` app for general purpose discussions.
- An app called `Konnekt` to find/search people with a certain required skill set.
### Installation:
Requirements:
- Python 3 runtime
- Django 2.0.4
- Other dependencies in `requirements.txt`

Procedure:
- Install [python](https://www.python.org/downloads/) in your environment
- Use pip to install other dependencies from `requirements.txt`
- Change to `src` directory
- Make database migrations with `python manage.py makemigrations` followed by `python manage.py migrate`
- Create a superuser with `python manage.py createsuperuser`
- Run development server on localhost with `python manage.py runserver`
