# api-cct
Conner Case Technologies Python excercise

# Installing and setup

Flask microframework with PyJWT was used, so:
```sh
$ pip install flask flask-sqlalchemy psycopg2 flask-migrate Flask-API flask-script flask-bcrypt
$ pip install PyJWT
```

PostgresSQL is used as DB (running on default port 5432)

### Create test and production DBs
```sh
$ [sudo -u postgres] createdb test_db
$ [sudo -u postgres] createdb api_cct
```

### Migrate
```sh
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

# Running tests
```sh
$ python manage.py test
```
# Starting
```sh
python run.py
```

# Resulting api

### Users and auth
#### Adding a user:
Request URL (POST):
 /auth/register

Property Name |	Type |	Notes
--- | --- | ---
email |	string | Email as username
password |	string | User's password

#### Logging in:
Request URL (POST):
 /auth/login

### Restaurants and menu:
#### Adding a restaurant:
Request URL (POST):
 /restaurants

Property Name |	Type |	Notes
--- | --- | ---
Name |	string | Name of the Restaurant

#### Getting a restaurant by id:
Request URL (GET):
 /restaurants/{id}

 #### Getting list og all restaurants:
Request URL (GET):
  /restaurants






