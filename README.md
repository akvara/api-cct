# api-cct
Conner Case Technologies Python excercise

# Flask microframework was used, so:
pip install flask flask-sqlalchemy psycopg2 flask-migrate Flask-API Flask-Script

# PostgresSQL is used as DB (running on default port 5432)

# Create test and production DBs
[sudo -u postgres] createdb test_db
[sudo -u postgres] createdb api_cct

# Migrate
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# Running tests
python test_api.py

# Start
python run.py

# Resulting api

## Adding a restaurant:
Request URL (POST):
 /restaurants

Property Name |	Type |	Notes
--- | --- | ---
Name |	string | Name of the Restaurant

## Getting a restaurant by id:
Request URL (GET):
 /restaurants/{id}

 ## Getting list og all restaurants:
Request URL (GET):
 /restaurants


