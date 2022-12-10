#!/bin/bash
./wait-for-it.sh postgres_db:5432 -- poetry run python manage.py runserver 0.0.0.0:8080
