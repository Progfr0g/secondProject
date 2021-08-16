#!/usr/bin/bash

pipenv run flake8 .
pipenv run isort .
pipenv run black .