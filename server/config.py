from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))

try:
    load_dotenv(path.join(basedir, '.env'))
except:
    print('Could not find .env. Assuming environment variables are already set')


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    OPENAI_API_KEY = environ.get('OPENAI_API_KEY')