# Barebones Flask Application
Barebones Flask application with a SQLite database, 1 blueprint and HTML base page using templates.
1 Database table and a single page to add entries to the database.
Can be used as a basepoint for further FLASK app development

## Setup for linux
1. cd into repo folder
2. Make virtual environment `python3 -m venv venv`
3. Activate environment `source venv/bin/activate`
4. Install packages `pip install -r requirements.txt`
5. Create environment variable `sudo nano webApp/.env`
```
SECRET_KEY = RANDOM_STRING
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
```
6. `export FLASK_APP=run.py`
7. Initialize database `flask db init`
8. Migrate  `flask db migrate -m "Initial migration."`
9. Update `flask db upgrade`

## How to run the app locally
1. Navigate to repo folder
2. Activate environment `source venv/bin/activate`
3. `set FLASK_APP=run.py`
4. Run with debug mode `flask --debug run`
