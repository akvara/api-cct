# api-cct
Conner Case Technologies Python excercise

# Flask microframework was used, so:
pip install flask flask-sqlalchemy psycopg2 flask-migrate Flask-API

# PostgresSQL is used as DB (running on default port 5432)

# Create test and production DBs
[sudo -u postgres] createdb test_db
[sudo -u postgres] createdb api_cct

# Start
python run.py