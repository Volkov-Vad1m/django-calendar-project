# django-calendar

A simple calendar application for Django.

## Installation
1. Perform a git clone of this repository.
2. Run the following command to deploy db:
```bash
cd docker/
docker-compose up
```
3. Run the following command to create the database:
```bash
cd ../django-calendar/
python manage.py migrate
```
4. Run the following command to create a superuser:
```bash
python manage.py createsuperuser <name>
```
5. Run the following command to create a token for the user:
```bash
python manage.py drf_create_token <username>
```
use the token to authenticate the user. You need to add the token in the header of the request as follows:
```
Authorization: Token <token>
```
6. Run the following command to start the server:
```bash
python manage.py runserver
```